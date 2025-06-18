# backend/load_data.py
from db import SessionLocal, engine
from models import Base, Patient
from fhir_parser import parse_patient_data

# 1. Create tables
Base.metadata.create_all(bind=engine)

# 2. Parse FHIR JSONs
data_folder = "../dataset"  # adjust if needed
patients = parse_patient_data(data_folder)

# 3. Insert into DB
session = SessionLocal()

for p in patients:
    patient = Patient(**p)
    session.merge(patient)  # merge = insert or update
session.commit()
session.close()

print(f"✅ Loaded {len(patients)} patients into database.")
