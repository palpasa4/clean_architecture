from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.config.postgresdb import Base


class AdminSchema(Base):
    __tablename__ = "admin_data"

    admin_id = Column(String, primary_key=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    fullname = Column(String, index=True)
    email = Column(String, index=True)
    role = Column(String, index=True)
