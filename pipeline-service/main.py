from fastapi import FastAPI, HTTPException
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

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()
    offset = (page - 1) * limit

    customers = db.query(Customer).offset(offset).limit(limit).all()

    return [to_dict(c) for c in customers]


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    customer = db.get(Customer, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return to_dict(customer)