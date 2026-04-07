# Backend Developer Technical Assessment

## 📌 Overview

This project implements a simple **data pipeline architecture** using:

- **Flask** — Mock API serving customer data
- **FastAPI** — Data ingestion & query service
- **PostgreSQL** — Persistent data storage
- **Docker Compose** — Service orchestration

---

## 🔄 Data Flow

Flask API → FastAPI Ingestion → PostgreSQL → API Response

This design ensures that data is **not directly served from the source**, but instead processed and stored before being accessed.

---

## 🚀 How to Run

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd backend-assessment
```

---

### 2. Run All Services

```bash
docker-compose up --build
```

Wait until all services are running:

- Flask → http://localhost:5000
- FastAPI → http://localhost:8000

---

## 🧪 API Usage

### 1. Get Mock Data (Flask)

```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

---

### 2. Ingest Data into PostgreSQL

```bash
curl -X POST http://localhost:8000/api/ingest
```

---

### 3. Get Customers (from Database)

```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

### 4. Get Customer by ID

```bash
curl http://localhost:8000/api/customers/CUST001
```

---

## ⚠️ Important Note

Before querying customer data, you **must run ingestion first**:

```bash
POST /api/ingest
```

This step loads data from the Flask mock API into PostgreSQL.

---

## 🏗️ Project Structure

```
backend-assessment/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── Dockerfile
    └── requirements.txt
```

---

## 🧠 Design Decisions

- **Data Ingestion Layer**
  Data is fetched from Flask and stored in PostgreSQL instead of being directly served.

- **Separation of Concerns**
  Each service has a single responsibility:
  - Flask → Data source
  - FastAPI → Processing & API
  - PostgreSQL → Storage

- **Upsert Strategy**
  Prevents duplicate records by updating existing entries.

---

## ✅ Features

- RESTful API design
- Pagination support
- Data ingestion pipeline
- PostgreSQL integration
- Dockerized multi-service architecture
- Error handling & basic validation

---

## 🛠️ Tech Stack

- Python 3.10+
- Flask
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose

---

## 🏁 Conclusion

This project demonstrates a simple yet effective **data pipeline architecture**, highlighting:

- Service orchestration
- API design
- Database integration
- Data processing workflow

## 🔧 Improvements (Future Work)

- Add authentication
- Implement async ingestion
- Add unit testing
- Use environment variables for configuration

---

## 📌 Author

Jordi Setiawan
