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

class Condition(Base):
    __tablename__ = "conditions"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    encounter_id = Column(String, ForeignKey("encounters.id"), nullable=True)
    clinical_status = Column(String)
    verification_status = Column(String)
    category = Column(String)
    code = Column(String)
    description = Column(String)
    onset_date = Column(DateTime)
    recorded_date = Column(DateTime)

class Observation(Base):
    __tablename__ = "observations"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    encounter_id = Column(String, ForeignKey("encounters.id"), nullable=True)
    status = Column(String)
    category = Column(String)
    code = Column(String)
    description = Column(String)
    value = Column(String)  # or Float if strictly numeric
    unit = Column(String)
    effective_date = Column(DateTime)
    issued_date = Column(DateTime)

class Medication(Base):
    __tablename__ = "medications"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    encounter_id = Column(String, ForeignKey("encounters.id"), nullable=True)
    medication_code = Column(String)
    medication_name = Column(String)
    status = Column(String)
    intent = Column(String)
    category = Column(String)
    authored_on = Column(DateTime)
    reason = Column(String)

class ImagingStudy(Base):
    __tablename__ = "imaging_studies"

    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    encounter_id = Column(String, ForeignKey("encounters.id"), nullable=True)
    status = Column(String)
    started = Column(DateTime)
    procedure_code = Column(String)
    procedure_display = Column(String)
    modality_code = Column(String)
    modality_display = Column(String)
    body_site = Column(String)
    dicom_uid = Column(String)