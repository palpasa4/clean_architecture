from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.modules.infrastructure.persistence.database import Base


class UserSchema(Base):
    __tablename__ = "user_data"

    cust_id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)


class BankAccount(Base):
    __tablename__ = "bank_acc"

    bank_acc_id = Column(String, primary_key=True, index=True)
    fullname = Column(String, index=True)
    address = Column(String, index=True)
    contact_no = Column(String, index=True)
    balance = Column(Float, index=True)
    cust_id = Column(String, ForeignKey("user_data.cust_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now())


class Transactions(Base):
    __tablename__ = "transaction_history"

    transaction_id = Column(String, primary_key=True, index=True)
    bank_acc_id = Column(String, ForeignKey("bank_acc.bank_acc_id"), nullable=False)
    transaction_type = Column(String, index=True)
    amount = Column(Float, index=True)
    previous_balance = Column(Float, index=True)
    new_balance = Column(Float, index=True)
    timestamp = Column(DateTime)

