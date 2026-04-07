from fastapi import FastAPI
from database import engine, Base

app = FastAPI()

# Create table
# Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "FastAPI is running"}