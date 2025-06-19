# backend/models.py
from sqlalchemy import Column, String, Date, ForeignKey, DateTime
from db import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    prefix = Column(String)
    gender = Column(String)
    birth_date = Column(Date)
    birth_sex = Column(String)
    race = Column(String)
    ethnicity = Column(String)
    marital_status = Column(String)
    language = Column(String)
    phone = Column(String)
    address_line = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String)


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    status = Column(String)
    class_code = Column(String)
    type_text = Column(String)
    reason = Column(String)
    location_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)