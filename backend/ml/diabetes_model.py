# backend/ml/diabetes_model.py

import joblib
import numpy as np
from db import SessionLocal
from models import Observation, Patient
from datetime import datetime

# Load trained diabetes model
MODEL_PATH = "train/models/diabetes_model.pkl"
diabetes_model = joblib.load(MODEL_PATH)

def predict_diabetes(patient_id: str):
    db = SessionLocal()
    try:
        # --- Feature 1: Glucose ---
        glucose = None
        glucose_obs = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.description.ilike('%glucose%'),
            Observation.value != None
        ).all()
        for obs in glucose_obs:
            try:
                glucose = float(obs.value)
                print(f"✅ Found glucose: {glucose}")
                break
            except:
                continue

        # --- Feature 2: Systolic Blood Pressure ---
        blood_pressure = None
        systolic_obs = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.description.ilike('%systolic%'),
            Observation.value != None
        ).all()
        for obs in systolic_obs:
            try:
                blood_pressure = float(obs.value)
                print(f"✅ Found systolic blood pressure: {blood_pressure}")
                break
            except:
                continue

        # --- Feature 3: BMI ---
        bmi = None
        bmi_obs = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.description.ilike('%bmi%'),
            Observation.value != None
        ).all()
        for obs in bmi_obs:
            try:
                bmi = float(obs.value)
                print(f"✅ Found BMI: {bmi}")
                break
            except:
                continue

        # --- Feature 4: Age from birth_date ---
        age = None
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient and patient.birth_date:
            today = datetime.today().date()
            age = today.year - patient.birth_date.year - (
                (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)
            )
            print(f"✅ Calculated age: {age}")

        # --- Final feature check ---
        features_found = {
            "glucose": glucose,
            "blood_pressure": blood_pressure,
            "bmi": bmi,
            "age": age
        }

        if None in [glucose, blood_pressure, bmi, age]:
            print("⚠️ Insufficient data for prediction.")
            return {
                "patient_id": patient_id,
                "status": "insufficient data",
                "features_found": features_found
            }

        # --- Predict diabetes ---
        X = np.array([[glucose, blood_pressure, bmi, age]])
        prediction = diabetes_model.predict(X)[0]
        prob = diabetes_model.predict_proba(X)[0][1]

        print(f"✅ Prediction complete. Probability: {prob:.3f}")

        return {
            "patient_id": patient_id,
            "status": "diabetic" if prediction == 1 else "non-diabetic",
            "confidence": round(prob, 3),
            "features_used": features_found
        }

    finally:
        db.close()
