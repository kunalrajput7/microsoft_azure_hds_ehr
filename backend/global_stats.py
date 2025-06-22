# backend/global_stats.py

from db import SessionLocal
from models import Patient, Condition, Medication, Encounter, ImagingStudy, PatientObservationSummary
from sqlalchemy import func, Float, cast
from datetime import date


def get_global_stats():
    db = SessionLocal()
    try:
        # --- Gender distribution ---
        gender_data = db.query(Patient.gender, func.count()).group_by(Patient.gender).all()
        gender = {g or "unknown": c for g, c in gender_data}

        # --- Race distribution ---
        race_data = db.query(Patient.race, func.count()).group_by(Patient.race).all()
        race = {r or "unknown": c for r, c in race_data}

        # --- Top 10 Conditions ---
        condition_data = db.query(Condition.description, func.count()).group_by(Condition.description).order_by(func.count().desc()).limit(10).all()
        top_conditions = [{"condition": desc or "unknown", "count": c} for desc, c in condition_data]

        # --- Top 10 Medications ---
        med_data = db.query(Medication.medication_name, func.count()).group_by(Medication.medication_name).order_by(func.count().desc()).limit(10).all()
        top_medications = [{"medication": name or "unknown", "count": c} for name, c in med_data]

        # --- Encounter type distribution ---
        encounter_data = db.query(Encounter.class_code, func.count()).group_by(Encounter.class_code).all()
        encounter_types = {code or "unknown": c for code, c in encounter_data}

        # --- Imaging modalities ---
        modality_data = db.query(ImagingStudy.modality_display, func.count()).group_by(ImagingStudy.modality_display).all()
        imaging_modality = {m or "unknown": c for m, c in modality_data}

        # --- Average vitals ---
        vitals_query = db.query(
            func.avg(cast(func.nullif(PatientObservationSummary.glucose, ''), Float)),
            func.avg(cast(func.nullif(PatientObservationSummary.bmi, ''), Float)),
            func.avg(cast(func.nullif(PatientObservationSummary.systolic_bp, ''), Float)),
            func.avg(cast(func.nullif(PatientObservationSummary.diastolic_bp, ''), Float))
        ).first()

        vitals_summary = {
            "avg_glucose": round(vitals_query[0], 2) if vitals_query[0] else None,
            "avg_bmi": round(vitals_query[1], 2) if vitals_query[1] else None,
            "avg_systolic": round(vitals_query[2], 2) if vitals_query[2] else None,
            "avg_diastolic": round(vitals_query[3], 2) if vitals_query[3] else None
        }

        return {
            "gender_distribution": gender,
            "race_distribution": race,
            "top_conditions": top_conditions,
            "top_medications": top_medications,
            "encounter_types": encounter_types,
            "imaging_modalities": imaging_modality,
            "vitals_summary": vitals_summary
        }

    finally:
        db.close()
