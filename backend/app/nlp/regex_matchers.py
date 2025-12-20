import re

# --------------------------------------------------
# Patient fields
# --------------------------------------------------
def extract_patient_fields(text: str) -> dict:
    data = {}

    age = re.search(r"Age:\s*(\d+)", text, re.IGNORECASE)
    gender = re.search(r"Gender:\s*(Male|Female)", text, re.IGNORECASE)
    weight = re.search(r"Weight:\s*(\d+)\s*(kg)", text, re.IGNORECASE)
    height = re.search(r"Height:\s*(\d+)\s*(cm)", text, re.IGNORECASE)

    if age:
        data["patient_onset_age__v"] = age.group(1)
        data["patient_age_unit__v"] = "Years"

    if gender:
        data["gender__v"] = gender.group(1)

    if weight:
        data["weight_value__v"] = weight.group(1)
        data["weight_unit__v"] = weight.group(2)

    if height:
        data["height_value__v"] = height.group(1)
        data["height_unit__v"] = height.group(2)

    data["patient_medical_history__v"] = ""

    return data


# --------------------------------------------------
# Drug name (CRITICAL FIX)
# --------------------------------------------------
def extract_drug_name(text: str) -> str:
    """
    Extracts drug name from structured fields like:
    'Suspect Drug: Atorvastatin 20 mg'
    """
    match = re.search(
        r"Suspect Drug:\s*([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE
    )
    return match.group(1) if match else ""

def extract_ck_lab(text: str) -> list:
    import re
    match = re.search(r"CK Levels:\s*(\d+)\s*U/L", text, re.IGNORECASE)
    if match:
        return [{
            "test_name": "Creatine Kinase",
            "value": match.group(1),
            "unit": "U/L",
            "abnormal_flag": "High"
        }]
    return []

def extract_event_fields(text: str) -> dict:
    data = {}

    event = re.search(r"Event Reported:\s*(.+)", text, re.IGNORECASE)
    onset = re.search(r"Onset Date:\s*(.+)", text, re.IGNORECASE)
    outcome = re.search(r"Outcome:\s*(.+)", text, re.IGNORECASE)

    if event:
        data["event_reported__v"] = event.group(1).strip()

    if onset:
        data["onset_idate__v"] = onset.group(1).strip()

    if outcome:
        data["outcome__v"] = outcome.group(1).strip()

    return data
