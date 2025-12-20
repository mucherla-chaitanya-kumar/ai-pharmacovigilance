from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Import ingestion orchestrator (absolute import)
from app.ingestion.ingestion import ingest_uploaded_files

app = FastAPI(title="AI-Powered Pharmacovigilance API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for uploaded files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    """Simple endpoint to verify backend is running."""
    return {"status": "ok", "message": "Backend is running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handles upload, stores file, and triggers ingestion."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Pass uploaded file to ingestion
    extracted_data = ingest_uploaded_files(file_path)

    response = [{
        "filename": file.filename,
        "text_preview": extracted_data[0]["text"][:500] if extracted_data else ""
    }]

    return {"status": "success", "files": response}
