# backend/ml/readmission_model.py

import joblib
import numpy as np
from db import SessionLocal
from models import Encounter, Observation, Patient, Condition, Medication, ImagingStudy
from datetime import datetime

# Load model
model = joblib.load("train/models/readmission_model.pkl")

def predict_readmission(patient_id: str):
    db = SessionLocal()
    try:
        today = datetime.today()

        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient or not patient.birth_date:
            return {"status": "insufficient data", "reason": "Missing patient birth date"}

        age = today.year - patient.birth_date.year - ((today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
        gender = 1 if patient.gender and patient.gender.lower() == "male" else 0

        encounters = db.query(Encounter).filter(Encounter.patient_id == patient_id).order_by(Encounter.start_time).all()
        if len(encounters) < 1:
            return {"status": "insufficient data", "reason": "No encounters"}

        num_prior = len(encounters)
        durations = [(e.end_time - e.start_time).days for e in encounters if e.end_time and e.start_time]
        avg_encounter_days = np.mean(durations) if durations else 1
        last_discharge = encounters[-1].end_time
        days_since_last = (today - last_discharge).days if last_discharge else 30

        conditions = db.query(Condition).filter(Condition.patient_id == patient_id).all()
        chronic_keywords = ["diabetes", "asthma", "copd", "hypertension", "chronic"]
        chronic_count = sum(1 for c in conditions if any(k in (c.description or "").lower() for k in chronic_keywords))

        obs = db.query(Observation).filter(Observation.patient_id == patient_id).all()
        glucose = next((float(o.value) for o in obs if o.description and 'glucose' in o.description.lower() and o.value), 100)
        bmi = next((float(o.value) for o in obs if o.description and 'bmi' in o.description.lower() and o.value), 25)
        systolic = next((float(o.value) for o in obs if o.description and 'systolic' in o.description.lower() and o.value), 130)

        meds = db.query(Medication).filter(Medication.patient_id == patient_id).count()
        imaging = db.query(ImagingStudy).filter(ImagingStudy.patient_id == patient_id).count()

        features = {
            "age": age,
            "gender": gender,
            "num_prior_encounters": num_prior,
            "avg_encounter_days": avg_encounter_days,
            "days_since_last_discharge": days_since_last,
            "num_chronic_conditions": chronic_count,
            "glucose": glucose,
            "systolic_bp": systolic,
            "bmi": bmi,
            "medication_count": meds,
            "imaging_count": imaging
        }

        X = np.array([[features[k] for k in features]])
        prediction = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

        return {
            "patient_id": patient_id,
            "status": "high-risk" if prediction == 1 else "low-risk",
            "confidence": round(prob, 3),
            "features_used": features
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
