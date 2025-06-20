import os
import pydicom
from datetime import datetime

def parse_dicom_data(folder_path, base_folder=""):
    dicom_data = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(".dcm"):
                continue

            full_path = os.path.join(root, file)
            try:
                ds = pydicom.dcmread(full_path)

                image_id = file.replace(".dcm", "")
                patient_id = getattr(ds, "PatientID", None)
                study_date = getattr(ds, "StudyDate", None)
                modality = getattr(ds, "Modality", None)

                # Convert date to datetime object
                if study_date:
                    try:
                        study_date = datetime.strptime(study_date, "%Y%m%d")
                    except:
                        study_date = None

                relative_path = os.path.relpath(full_path, base_folder)

                dicom_data.append({
                    "id": image_id,
                    "patient_id": patient_id,
                    "file_path": relative_path,
                    "study_date": study_date,
                    "modality": modality,
                    "prediction": None
                })

            except Exception as e:
                print(f"❌ Error reading {full_path}: {e}")

    return dicom_data
