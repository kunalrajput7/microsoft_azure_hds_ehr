# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from ml.glucose_model import predict_glucose_anomalies
from db import SessionLocal, engine
from models import (
    Patient, Encounter, Condition, Observation,
    Medication, ImagingStudy, DICOMImage
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EHR API",
    description="FHIR + DICOM Metadata API with AI Readiness",
    version="1.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- ROOT ----------
@app.get("/")
def root():
    return {"message": "Welcome to the EHR API 🚀"}

# ---------- PATIENTS ----------
@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ---------- ENCOUNTERS ----------
@app.get("/encounters")
def get_encounters(db: Session = Depends(get_db)):
    return db.query(Encounter).all()

@app.get("/encounters/{patient_id}")
def get_encounters_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Encounter).filter(Encounter.patient_id == patient_id).all()

# ---------- CONDITIONS ----------
@app.get("/conditions")
def get_conditions(db: Session = Depends(get_db)):
    return db.query(Condition).all()

@app.get("/conditions/{patient_id}")
def get_conditions_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Condition).filter(Condition.patient_id == patient_id).all()

# ---------- OBSERVATIONS ----------
@app.get("/observations")
def get_observations(db: Session = Depends(get_db)):
    return db.query(Observation).all()

@app.get("/observations/{patient_id}")
def get_observations_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Observation).filter(Observation.patient_id == patient_id).all()

# ---------- MEDICATIONS ----------
@app.get("/medications")
def get_medications(db: Session = Depends(get_db)):
    return db.query(Medication).all()

@app.get("/medications/{patient_id}")
def get_medications_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(Medication).filter(Medication.patient_id == patient_id).all()

# ---------- IMAGING STUDIES ----------
@app.get("/imaging-studies")
def get_imaging_studies(db: Session = Depends(get_db)):
    return db.query(ImagingStudy).all()

@app.get("/imaging-studies/{patient_id}")
def get_imaging_studies_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(ImagingStudy).filter(ImagingStudy.patient_id == patient_id).all()

# ---------- DICOM METADATA ----------
@app.get("/dicom-images")
def get_all_dicom_images(db: Session = Depends(get_db)):
    return db.query(DICOMImage).all()

@app.get("/dicom-images/{patient_id}")
def get_dicom_images_by_patient(patient_id: str, db: Session = Depends(get_db)):
    return db.query(DICOMImage).filter(DICOMImage.patient_id == patient_id).all()


@app.get("/predict-glucose/{patient_id}")
def glucose_prediction(patient_id: str):
    result = predict_glucose_anomalies(patient_id)
    return result