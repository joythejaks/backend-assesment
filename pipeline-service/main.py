from fastapi import FastAPI
from database import engine, Base
from services.ingestion import fetch_all_customers
from database import SessionLocal
from models.customer import Customer

app = FastAPI()

# Create table
# Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.post("/api/ingest")
def ingest():
    customers = fetch_all_customers()

    return {
        "status": "success",
        "records_processed": len(customers)
    }