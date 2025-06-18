# backend/fhir_parser.py
import os, json
from fhir.resources.patient import Patient as FHIRPatient

def parse_patient_data(folder_path):
    patients = []
    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") == "Patient":
                    try:
                        patient = FHIRPatient.parse_obj(resource)

                        name = (patient.name[0].given[0] + " " + patient.name[0].family) if patient.name else "Unknown"
                        birth_date = patient.birthDate if patient.birthDate else None

                        patients.append({
                            "id": patient.id,
                            "name": name,
                            "gender": patient.gender,
                            "birthdate": birth_date
                        })
                    except Exception as e:
                        print(f"Error parsing Patient in {filename}: {e}")
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
    return patients
