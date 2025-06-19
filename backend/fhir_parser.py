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

                try:
                    observation_id = resource.get("id")
                    patient_ref = resource.get("subject", {}).get("reference", "")
                    patient_id = patient_ref.replace("urn:uuid:", "") if patient_ref else None

                    encounter_ref = resource.get("encounter", {}).get("reference", "")
                    encounter_id = encounter_ref.replace("urn:uuid:", "") if encounter_ref else None

                    status = resource.get("status")

                    category = resource.get("category", [{}])[0].get("coding", [{}])[0].get("code")

                    code = resource.get("code", {}).get("coding", [{}])[0].get("code")
                    description = resource.get("code", {}).get("coding", [{}])[0].get("display")

                    value_quantity = resource.get("valueQuantity", {})
                    value = value_quantity.get("value")
                    unit = value_quantity.get("unit")

                    effective = resource.get("effectiveDateTime")
                    issued = resource.get("issued")

                    effective_date = datetime.fromisoformat(effective) if effective else None
                    issued_date = datetime.fromisoformat(issued) if issued else None

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
                    print(f"Error parsing Observation in {filename}: {e}")

        except Exception as e:
            print(f"Error reading file {filename}: {e}")

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