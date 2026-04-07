from fastapi import FastAPI
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import fetch_all_customers

app = FastAPI()

# create table
Base.metadata.create_all(bind=engine)


@app.post("/api/ingest")
def ingest():
    db = SessionLocal()

    try:
        customers = fetch_all_customers()
        processed = 0

        for item in customers:
            existing = db.get(Customer, item["customer_id"])

            if existing:
                # 🔄 UPDATE (UPSERT)
                for key, value in item.items():
                    setattr(existing, key, value)
            else:
                # ➕ INSERT
                new_customer = Customer(**item)
                db.add(new_customer)

            processed += 1

        db.commit()

        return {
            "status": "success",
            "records_processed": processed
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()