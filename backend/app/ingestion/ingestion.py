import os
from .pdf_reader import extract_text_from_pdf
from .ocr_extractor import extract_text_with_ocr

UPLOAD_DIR = "./uploads"  # adjust relative path

def ingest_uploaded_files(file_path=None):
    all_data = []

    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            text = extract_text_from_pdf(file_path)

        elif ext in ["jpg", "jpeg", "png", "tiff"]:
            text = extract_text_with_ocr(file_path)

        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        all_data.append({
            "filename": filename,
            "text": text
        })

    return all_data
