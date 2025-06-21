# backend/fhir_parser.py
import os, json
from datetime import datetime
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.encounter import Encounter as FHIREncounter

def extract_extension_value(extensions, url_substring):
    for ext in extensions:
        if url_substring in ext.get("url", ""):
            # Case 1: nested structure (like race, ethnicity)
            if "extension" in ext:
                for sub in ext["extension"]:
                    if "valueString" in sub:
                        return sub["valueString"]
                    elif "valueCode" in sub:
                        return sub["valueCode"]
            # Case 2: flat valueCode/valueString directly
            if "valueString" in ext:
                return ext["valueString"]
            if "valueCode" in ext:
                return ext["valueCode"]
    return None

# THIS FUNCTION WILL EXTRACT THE PATIENT DATA FROM EVERY FHIR DOCUMENT
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
                if resource.get("resourceType") != "Patient":
                    continue

                try:
                    patient = FHIRPatient.parse_obj(resource)

                    # Name
                    name_data = patient.name[0] if patient.name else None
                    full_name = f"{name_data.given[0]} {name_data.family}" if name_data else "Unknown"
                    prefix = name_data.prefix[0] if name_data and name_data.prefix else None

                    # Extensions
                    extensions = resource.get("extension", [])
                    birth_sex = extract_extension_value(extensions, "sex")
                    race = extract_extension_value(extensions, "race")
                    ethnicity = extract_extension_value(extensions, "ethnicity")

                    # Address
                    addr = patient.address[0] if patient.address else None
                    address_line = addr.line[0] if addr and addr.line else None
                    city = addr.city if addr else None
                    state = addr.state if addr else None
                    postal_code = addr.postalCode if addr else None
                    country = addr.country if addr else None

                    # Others
                    marital_status = patient.maritalStatus.text if patient.maritalStatus else None
                    language = patient.communication[0].language.text if patient.communication else None
                    phone = patient.telecom[0].value if patient.telecom else None
                    if patient.birthDate:
                        birth_date = patient.birthDate if isinstance(patient.birthDate, datetime) else datetime.strptime(str(patient.birthDate), "%Y-%m-%d").date()
                    else:
                        birth_date: None


                    patients.append({
                        "id": patient.id,
                        "full_name": full_name,
                        "prefix": prefix,
                        "gender": patient.gender,
                        "birth_date": birth_date,
                        "birth_sex": birth_sex,
                        "race": race,
                        "ethnicity": ethnicity,
                        "marital_status": marital_status,
                        "language": language,
                        "phone": phone,
                        "address_line": address_line,
                        "city": city,
                        "state": state,
                        "postal_code": postal_code,
                        "country": country
                    })

                except Exception as e:
                    print(f"Error parsing Patient in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return patients


# THIS FUNCTION WILL EXTRACT ALL THE ENCOUNTER DATA OF EACH PATIENT FROM THE FHIR DOCUMENT

def parse_encounter_data(folder_path):
    encounters = []

    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") != "Encounter":
                    continue

                try:
                    # ID
                    encounter_id = resource.get("id")

                    # Patient ID (remove "urn:uuid:")
                    subject = resource.get("subject", {})
                    patient_ref = subject.get("reference", "")
                    patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                    # Status & class
                    status = resource.get("status")
                    class_code = resource.get("class", {}).get("code")

                    # Type text
                    type_list = resource.get("type", [])
                    type_text = type_list[0].get("text") if type_list else None

                    # Reason
                    reason_list = resource.get("reasonCode", [])
                    reason = reason_list[0]["coding"][0]["display"] if reason_list and "coding" in reason_list[0] else None

                    # Location name
                    location = resource.get("location", [])
                    location_name = location[0]["location"]["display"] if location and "location" in location[0] else None

                    # Time period
                    period = resource.get("period", {})
                    start_time = period.get("start")
                    end_time = period.get("end")

                    # Format timestamps
                    from datetime import datetime
                    start_dt = datetime.fromisoformat(start_time) if start_time else None
                    end_dt = datetime.fromisoformat(end_time) if end_time else None

                    # Append parsed encounter
                    encounters.append({
                        "id": encounter_id,
                        "patient_id": patient_id,
                        "status": status,
                        "class_code": class_code,
                        "type_text": type_text,
                        "reason": reason,
                        "location_name": location_name,
                        "start_time": start_dt,
                        "end_time": end_dt
                    })

                except Exception as e:
                    print(f"Error parsing Encounter in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return encounters


def parse_condition_data(folder_path):
    conditions = []

    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") != "Condition":
                    continue

                try:
                    condition_id = resource.get("id")
                    patient_ref = resource.get("subject", {}).get("reference", "")
                    patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                    encounter_ref = resource.get("encounter", {}).get("reference", "")
                    encounter_id = encounter_ref.replace("urn:uuid:", "") if encounter_ref else None

                    clinical_status = resource.get("clinicalStatus", {}).get("coding", [{}])[0].get("code")
                    verification_status = resource.get("verificationStatus", {}).get("coding", [{}])[0].get("code")
                    category = resource.get("category", [{}])[0].get("coding", [{}])[0].get("display")

                    code = resource.get("code", {}).get("coding", [{}])[0].get("code")
                    description = resource.get("code", {}).get("coding", [{}])[0].get("display")

                    onset = resource.get("onsetDateTime")
                    onset_date = datetime.fromisoformat(onset) if onset else None

                    recorded = resource.get("recordedDate")
                    recorded_date = datetime.fromisoformat(recorded) if recorded else None

                    conditions.append({
                        "id": condition_id,
                        "patient_id": patient_id,
                        "encounter_id": encounter_id,
                        "clinical_status": clinical_status,
                        "verification_status": verification_status,
                        "category": category,
                        "code": code,
                        "description": description,
                        "onset_date": onset_date,
                        "recorded_date": recorded_date
                    })

                except Exception as e:
                    print(f"Error parsing Condition in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return conditions


from datetime import datetime
import os, json

def parse_observation_data(folder_path):
    observations = []

    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") != "Observation":
                    continue

                observation_id = resource.get("id")
                patient_ref = resource.get("subject", {}).get("reference", "")
                patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                encounter_ref = resource.get("encounter", {}).get("reference", "")
                encounter_id = encounter_ref.replace("urn:uuid:", "") if encounter_ref else None

                status = resource.get("status")
                category = resource.get("category", [{}])[0].get("coding", [{}])[0].get("code")

                code_block = resource.get("code", {})
                code = code_block.get("coding", [{}])[0].get("code")
                description = code_block.get("coding", [{}])[0].get("display")

                effective = resource.get("effectiveDateTime")
                issued = resource.get("issued")
                effective_date = datetime.fromisoformat(effective) if effective else None
                issued_date = datetime.fromisoformat(issued) if issued else None

                # --- Case 1: Blood Pressure with components ---
                if description and "blood pressure" in description.lower() and "component" in resource:
                    for component in resource["component"]:
                        comp_code = component["code"]["coding"][0].get("code")
                        comp_desc = component["code"]["coding"][0].get("display")
                        comp_value = component.get("valueQuantity", {}).get("value")
                        comp_unit = component.get("valueQuantity", {}).get("unit")

                        if comp_value is not None:
                            observations.append({
                                "id": f"{observation_id}-{comp_code}",  # Make ID unique per component
                                "patient_id": patient_id,
                                "encounter_id": encounter_id,
                                "status": status,
                                "category": category,
                                "code": comp_code,
                                "description": comp_desc,
                                "value": comp_value,
                                "unit": comp_unit,
                                "effective_date": effective_date,
                                "issued_date": issued_date
                            })

                # --- Case 2: Normal observation like BMI, Glucose ---
                else:
                    value_quantity = resource.get("valueQuantity", {})
                    value = value_quantity.get("value")
                    unit = value_quantity.get("unit")

                    if value is not None:
                        observations.append({
                            "id": observation_id,
                            "patient_id": patient_id,
                            "encounter_id": encounter_id,
                            "status": status,
                            "category": category,
                            "code": code,
                            "description": description,
                            "value": value,
                            "unit": unit,
                            "effective_date": effective_date,
                            "issued_date": issued_date
                        })

        except Exception as e:
            print(f"⚠️ Error parsing {filename}: {e}")

    return observations


def parse_medication_data(folder_path):
    medications = []
    medication_lookup = {}

    # First pass: build a lookup for Medication resource (id → name/code)
    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
            data = json.load(f)

        for entry in data.get("entry", []):
            resource = entry.get("resource", {})
            if resource.get("resourceType") == "Medication":
                med_id = resource.get("id")
                code = resource.get("code", {}).get("coding", [{}])[0].get("code")
                name = resource.get("code", {}).get("coding", [{}])[0].get("display")
                medication_lookup[med_id] = {
                    "code": code,
                    "name": name
                }

    # Second pass: extract MedicationRequest and join with Medication
    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") != "MedicationRequest":
                    continue

                try:
                    med_id = resource.get("id")
                    patient_ref = resource.get("subject", {}).get("reference", "")
                    patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                    encounter_ref = resource.get("encounter", {}).get("reference", "")
                    encounter_id = encounter_ref.replace("urn:uuid:", "") if encounter_ref else None

                    medication_ref = resource.get("medicationReference", {}).get("reference", "")
                    medication_uuid = medication_ref.replace("urn:uuid:", "") if medication_ref else None
                    med_data = medication_lookup.get(medication_uuid, {})

                    status = resource.get("status")
                    intent = resource.get("intent")
                    category = resource.get("category", [{}])[0].get("coding", [{}])[0].get("display")

                    authored_on_raw = resource.get("authoredOn")
                    authored_on = datetime.fromisoformat(authored_on_raw) if authored_on_raw else None

                    reason = resource.get("reasonReference", [{}])[0].get("display")

                    medications.append({
                        "id": med_id,
                        "patient_id": patient_id,
                        "encounter_id": encounter_id,
                        "medication_code": med_data.get("code"),
                        "medication_name": med_data.get("name"),
                        "status": status,
                        "intent": intent,
                        "category": category,
                        "authored_on": authored_on,
                        "reason": reason
                    })

                except Exception as e:
                    print(f"Error parsing MedicationRequest in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return medications

def parse_imaging_data(folder_path):
    imaging_studies = []

    for filename in os.listdir(folder_path):
        if not filename.endswith('.json'):
            continue

        try:
            with open(os.path.join(folder_path, filename), encoding="utf-8") as f:
                data = json.load(f)

            for entry in data.get("entry", []):
                resource = entry.get("resource", {})
                if resource.get("resourceType") != "ImagingStudy":
                    continue

                try:
                    study_id = resource.get("id")
                    patient_ref = resource.get("subject", {}).get("reference", "")
                    patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                    encounter_ref = resource.get("encounter", {}).get("reference", "")
                    encounter_id = encounter_ref.replace("urn:uuid:", "") if encounter_ref else None

                    status = resource.get("status")
                    started_raw = resource.get("started")
                    started = datetime.fromisoformat(started_raw) if started_raw else None

                    procedure_code = resource.get("procedureCode", [{}])[0].get("coding", [{}])[0].get("code")
                    procedure_display = resource.get("procedureCode", [{}])[0].get("coding", [{}])[0].get("display")

                    # Only taking first series for now
                    series = resource.get("series", [{}])[0]
                    modality_code = series.get("modality", {}).get("code")
                    modality_display = series.get("modality", {}).get("display")

                    body_site = series.get("bodySite", {}).get("display")
                    dicom_uid = series.get("uid")  # Series UID

                    imaging_studies.append({
                        "id": study_id,
                        "patient_id": patient_id,
                        "encounter_id": encounter_id,
                        "status": status,
                        "started": started,
                        "procedure_code": procedure_code,
                        "procedure_display": procedure_display,
                        "modality_code": modality_code,
                        "modality_display": modality_display,
                        "body_site": body_site,
                        "dicom_uid": dicom_uid
                    })

                except Exception as e:
                    print(f"Error parsing ImagingStudy in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return imaging_studies


# backend/fhir_summary_parser.py

from db import SessionLocal
from models import Observation, PatientObservationSummary
from sqlalchemy.orm import Session
from sqlalchemy import func

def generate_patient_observation_summary():
    db: Session = SessionLocal()
    try:
        print("🟡 Generating patient observation summaries...")

        # Get unique patient IDs from observations
        patient_ids = db.query(Observation.patient_id).distinct().all()

        for (patient_id,) in patient_ids:
            # Glucose
            glucose_obs = db.query(Observation).filter(
                Observation.patient_id == patient_id,
                Observation.description.ilike('%glucose%'),
                Observation.value != None
            ).order_by(Observation.effective_date.desc()).first()

            # BMI
            bmi_obs = db.query(Observation).filter(
                Observation.patient_id == patient_id,
                Observation.description.ilike('%bmi%'),
                Observation.value != None
            ).order_by(Observation.effective_date.desc()).first()

            # Systolic BP
            sys_obs = db.query(Observation).filter(
                Observation.patient_id == patient_id,
                Observation.description.ilike('%systolic%'),
                Observation.value != None
            ).order_by(Observation.effective_date.desc()).first()

            # Diastolic BP
            dia_obs = db.query(Observation).filter(
                Observation.patient_id == patient_id,
                Observation.description.ilike('%diastolic%'),
                Observation.value != None
            ).order_by(Observation.effective_date.desc()).first()

            summary = PatientObservationSummary(
                patient_id=patient_id,
                glucose=glucose_obs.value if glucose_obs else None,
                glucose_unit=glucose_obs.unit if glucose_obs else None,
                bmi=bmi_obs.value if bmi_obs else None,
                bmi_unit=bmi_obs.unit if bmi_obs else None,
                systolic_bp=sys_obs.value if sys_obs else None,
                systolic_unit=sys_obs.unit if sys_obs else None,
                diastolic_bp=dia_obs.value if dia_obs else None,
                diastolic_unit=dia_obs.unit if dia_obs else None,
            )

            db.merge(summary)  # Insert or update
        db.commit()
        print("✅ Patient observation summaries generated.")

    finally:
        db.close()
