import os
from .pdf_reader import extract_text_from_pdf
from .ocr_extractor import extract_text_from_image

UPLOAD_DIR = "./uploads"  # adjust relative path

def ingest_uploaded_files():
    all_data = []
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        ext = filename.lower().split(".")[-1]

        if ext == "pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in ["jpg", "jpeg", "png", "tiff"]:
            text = extract_text_from_image(file_path)
        else:
            # For txt or other formats
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        all_data.append({
            "filename": filename,
            "text": text
        })

    return all_data

if __name__ == "__main__":
    data = ingest_uploaded_files()
    for item in data:
        print(f"File: {item['filename']}")
        print(item['text'][:500])  # preview first 500 chars
        print("-" * 50)
