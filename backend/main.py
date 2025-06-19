# backend/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Patient

app = FastAPI(title="EHR API", description="FHIR-Powered Patient Data API", version="1.0")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route: Root
@app.get("/")
def root():
    return {"message": "Welcome to EHR API"}

# Route: Get all patients
@app.get("/patients")
def get_patients():
    db = next(get_db())
    patients = db.query(Patient).all()
    return patients

# Route: Get one patient by ID
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    db = next(get_db())
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
