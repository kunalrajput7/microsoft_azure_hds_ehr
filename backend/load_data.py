# backend/load_data.py
from db import SessionLocal, engine
from models import Base, Patient, Encounter
from fhir_parser import parse_patient_data, parse_encounter_data

# 1. Create all tables (only if not exist)
Base.metadata.create_all(bind=engine)

# 2. Parse FHIR JSONs
data_folder = "../dataset"
patients = parse_patient_data(data_folder)
encounters = parse_encounter_data(data_folder)

# 3. Insert into DB
session = SessionLocal()

# Insert patients
for p in patients:
    session.merge(Patient(**p))

# Insert encounters
for e in encounters:
    session.merge(Encounter(**e))

# Commit and close
session.commit()
session.close()

print(f"✅ Loaded {len(patients)} patients into database.")
print(f"✅ Loaded {len(encounters)} encounters into database.")
