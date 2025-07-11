# backend/load_data.py
import os
from db import SessionLocal, engine
from models import Base, DICOMImage, Patient, Encounter, Condition, Observation, Medication, ImagingStudy
from fhir_parser import parse_patient_data, parse_encounter_data, parse_condition_data, parse_observation_data, parse_medication_data, parse_imaging_data, generate_patient_observation_summary
from dicom_parser import parse_dicom_data

# 1. Create all tables (only if not exist)
Base.metadata.create_all(bind=engine)

# 2. Parse FHIR JSONs
data_folder = "../dataset"
patients = parse_patient_data(data_folder)
encounters = parse_encounter_data(data_folder)
conditions = parse_condition_data(data_folder)
observations = parse_observation_data(data_folder)
medications = parse_medication_data(data_folder)
imaging_studies = parse_imaging_data(data_folder)

# 3. Parse DICOM
dicom_folder = os.path.join(data_folder, "rsna/train_dicom")
dicoms = parse_dicom_data(dicom_folder, base_folder=data_folder)

# 4. Insert into DB
session = SessionLocal()

# Insert patients
for p in patients:
    session.merge(Patient(**p))

# Insert encounters
for e in encounters:
    session.merge(Encounter(**e))

# Insert conditions
for c in conditions:
    session.merge(Condition(**c))

for o in observations:
    session.merge(Observation(**o))

for m in medications:
    session.merge(Medication(**m))

for i in imaging_studies:
    session.merge(ImagingStudy(**i))

for d in dicoms:
    session.merge(DICOMImage(**d))
    
generate_patient_observation_summary()

# Commit and close
session.commit()
session.close()

print(f"✅ Loaded {len(patients)} patients into database.")
print(f"✅ Loaded {len(encounters)} encounters into database.")
print(f"✅ Loaded {len(conditions)} conditions into database.")
print(f"✅ Loaded {len(observations)} observations into database.")
print(f"✅ Loaded {len(medications)} medications into database.")
print(f"✅ Loaded {len(imaging_studies)} imaging studies into database.")
print(f"✅ Loaded {len(dicoms)} DICOM images.")
