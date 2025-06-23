# backend/patient_fhir_stats.py

from db import SessionLocal
from models import (
    Patient, Condition, Medication, Encounter,
    Observation, ImagingStudy, PatientObservationSummary
)
from sqlalchemy import func, cast, Float
from collections import defaultdict


def get_patient_fhir_stats(patient_id: str):
    db = SessionLocal()
    try:
        # --- Patient Demographics ---
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        patient_info = {
            "id": patient.id,
            "full_name": patient.full_name,
            "gender": patient.gender,
            "birth_date": str(patient.birth_date),
            "birth_sex": patient.birth_sex,
            "race": patient.race,
            "ethnicity": patient.ethnicity,
            "marital_status": patient.marital_status,
            "language": patient.language,
            "phone": patient.phone,
            "address_line": patient.address_line,
            "city": patient.city,
            "state": patient.state,
            "postal_code": patient.postal_code,
            "country": patient.country
        } if patient else {}

        # --- Conditions ---
        condition_data = db.query(
            Condition.description,
            func.count()
        ).filter(Condition.patient_id == patient_id).group_by(
            Condition.description
        ).order_by(func.count().desc()).limit(10).all()

        conditions = [{"condition": d or "unknown", "count": c} for d, c in condition_data]

        # --- Medications ---
        med_data = db.query(
            Medication.medication_name,
            func.count()
        ).filter(Medication.patient_id == patient_id).group_by(
            Medication.medication_name
        ).order_by(func.count().desc()).limit(10).all()

        medications = [{"medication": m or "unknown", "count": c} for m, c in med_data]

        # --- Encounter Types ---
        encounter_data = db.query(
            Encounter.class_code,
            func.count()
        ).filter(Encounter.patient_id == patient_id).group_by(
            Encounter.class_code
        ).all()

        encounters = {e or "unknown": c for e, c in encounter_data}

        # --- Encounter Timeline (Optional visualization) ---
        timeline_data = db.query(
            Encounter.start_time,
            Encounter.reason,
            Encounter.class_code
        ).filter(Encounter.patient_id == patient_id).order_by(Encounter.start_time.asc()).all()
        
        encounter_timeline = []
        for start, reason, class_code in timeline_data:
            if start:
                encounter_timeline.append({
                    "start": start.isoformat(),
                    "reason": reason or class_code or "Encounter"
                })

        # --- Imaging Modalities ---
        modality_data = db.query(
            ImagingStudy.modality_display,
            func.count()
        ).filter(ImagingStudy.patient_id == patient_id).group_by(
            ImagingStudy.modality_display
        ).all()

        imaging = {m or "unknown": c for m, c in modality_data}

        # --- Vitals Summary ---
        summary = db.query(PatientObservationSummary).filter(
            PatientObservationSummary.patient_id == patient_id
        ).first()

        vitals_summary = {
            "glucose": summary.glucose if summary else None,
            "bmi": summary.bmi if summary else None,
            "systolic_bp": summary.systolic_bp if summary else None,
            "diastolic_bp": summary.diastolic_bp if summary else None,
        }

        return {
            "patient_info": patient_info,
            "conditions": conditions,
            "medications": medications,
            "encounter_types": encounters,
            "encounter_timeline": encounter_timeline,
            "imaging_modalities": imaging,
            "vitals_summary": vitals_summary
        }

    finally:
        db.close()
