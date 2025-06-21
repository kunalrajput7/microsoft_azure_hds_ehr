# backend/ml/glucose_model.py

import joblib
import os
from db import SessionLocal
from models import Observation
import numpy as np

# Load trained model once
MODEL_PATH = os.path.join("train", "models", "glucose_model.pkl")
glucose_model = joblib.load(MODEL_PATH)

def predict_glucose_anomalies(patient_id: str):
    db = SessionLocal()
    try:
        # Get glucose observations for patient
        records = db.query(Observation).filter(
            Observation.patient_id == patient_id,
            Observation.description.ilike('%Glucose [Mass/volume] in Blood%'),
            Observation.value != None
        ).all()

        values = []
        for r in records:
            try:
                values.append(float(r.value))
            except:
                continue

        if not values:
            return {"message": "No valid glucose readings found."}

        X = np.array(values).reshape(-1, 1)
        preds = glucose_model.predict(X)  # -1 = anomaly, 1 = normal

        results = [
            {"value": v, "status": "anomaly" if p == -1 else "normal"}
            for v, p in zip(values, preds)
        ]
        return {"patient_id": patient_id, "predictions": results}

    finally:
        db.close()
