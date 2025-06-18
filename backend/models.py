# backend/models.py
from sqlalchemy import Column, String, Date
from db import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    gender = Column(String)
    birthdate = Column(Date)
