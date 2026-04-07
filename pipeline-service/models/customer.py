from sqlalchemy import Column, String, Date, Numeric, TIMESTAMP
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    date_of_birth = Column(Date)
    account_balance = Column(Numeric)
    created_at = Column(TIMESTAMP)