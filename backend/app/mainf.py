from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.ingestion.pdf_reader import extract_text_from_pdf
from app.nlp.regex_matchers import (
    extract_patient_fields,
    extract_drug_name,
    extract_ck_lab,
    extract_event_fields
)
from app.nlp.regex_dose import extract_dose_fields
from app.nlp.ner_pipeline import run_ner, postprocess_entities
from app.utils.case_mapper import map_case
from app.utils.validation import validate_semantic

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(title="AI Pharmacovigilance System")

# --------------------------------------------------
# CORS (React frontend)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Upload directory
# --------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# Core processing pipeline
# --------------------------------------------------
def process_pipeline(pdf_path: str):
    # 1. Extract text
    text = extract_text_from_pdf(pdf_path)

    # 2. Regex-based extraction (authoritative)
    patient_data = extract_patient_fields(text)
    dose_data = extract_dose_fields(text)
    drug_name = extract_drug_name(text)
    event_data = extract_event_fields(text)

    regex_data = {
        **patient_data,
        **dose_data,
        **event_data,
        "drug_name": drug_name
    }

    # 3. NER (optional enrichment, not authoritative)
    ner_raw = run_ner(text)
    ner_data = postprocess_entities(ner_raw)

    # 4. Map into case schema
    case = map_case(ner_data, regex_data)

    # 5. Labs (CK)
    labs = extract_ck_lab(text)
    case["labs"] = labs

    # 6. Validation
    validation = validate_semantic(case)

    return {
        "case": case,
        "validation": validation
    }

# --------------------------------------------------
# API endpoints
# --------------------------------------------------
@app.post("/process")
def process_aer(file: UploadFile = File(...)):
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return process_pipeline(pdf_path)


@app.post("/upload")
def upload_alias(file: UploadFile = File(...)):
    return process_aer(file)

@app.post("/narrative")
def generate_narrative(case: dict):
    patient = case.get("patient", {})
    drug = case.get("drug", {})
    event = case.get("event", {})
    labs = case.get("labs", [])

    ck_info = ""
    if labs:
        ck = labs[0]
        ck_info = (
            f" Laboratory tests showed elevated {ck.get('test_name')} "
            f"({ck.get('value')} {ck.get('unit')})."
        )

    narrative = (
        f"A {patient.get('patient_onset_age__v')} year old "
        f"{patient.get('gender__v')} patient was treated with "
        f"{drug.get('product_reported__v')} "
        f"{drug.get('dose_value__v')} {drug.get('dose_unit__v')} "
        f"{drug.get('frequency_value__v')} via "
        f"{drug.get('drug_route__v')}. "
        f"The patient experienced {event.get('event_reported__v')} "
        f"on {event.get('onset_idate__v')}. "
        f"Outcome was {event.get('outcome__v')}.{ck_info}"
    )

    return {"narrative": narrative}
