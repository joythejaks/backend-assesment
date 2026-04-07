from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import fetch_all_customers
from datetime import datetime


# ======================
# Lifespan (Startup Logic)
# ======================
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)

        customers = fetch_all_customers()

        for item in customers:
            # Convert date fields
            item["date_of_birth"] = datetime.strptime(item["date_of_birth"], "%Y-%m-%d")
            item["created_at"] = datetime.fromisoformat(item["created_at"])

            existing = db.get(Customer, item["customer_id"])
            if not existing:
                db.add(Customer(**item))

        db.commit()
        print(f"[Startup] Seeded {len(customers)} customers")

    except Exception as e:
        print(f"[Startup Error] {e}")
        db.rollback()
    finally:
        db.close()

    yield


app = FastAPI(lifespan=lifespan)


# ======================
# Helper
# ======================
def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


# ======================
# Ingest Endpoint
# ======================
@app.post("/api/ingest")
def ingest():
    db = SessionLocal()

    try:
        customers = fetch_all_customers()
        processed = 0

        for item in customers:
            # Convert date fields
            item["date_of_birth"] = datetime.strptime(item["date_of_birth"], "%Y-%m-%d")
            item["created_at"] = datetime.fromisoformat(item["created_at"])

            existing = db.get(Customer, item["customer_id"])

            if existing:
                # UPSERT (update)
                for key, value in item.items():
                    setattr(existing, key, value)
            else:
                # INSERT
                db.add(Customer(**item))

            processed += 1

        db.commit()

        print(f"[Ingest] Processed {processed} records")

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


# ======================
# Get Customers (Pagination)
# ======================
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()

    try:
        offset = (page - 1) * limit
        customers = db.query(Customer).offset(offset).limit(limit).all()
        return [to_dict(c) for c in customers]

    finally:
        db.close()


# ======================
# Get Customer by ID
# ======================
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    try:
        customer = db.get(Customer, customer_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return to_dict(customer)

    finally:
        db.close()


# ======================
# Health Check
# ======================
@app.get("/api/health")
def health():
    return {"status": "ok"}

