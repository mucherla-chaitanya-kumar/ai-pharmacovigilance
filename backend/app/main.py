from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Import ingestion orchestrator
from .ingestion.ingestion import ingest_uploaded_files

app = FastAPI()

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for storing uploaded files
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Call ingestion module to extract text
    extracted_data = ingest_uploaded_files()

    # Return JSON response: list of all uploaded files and text preview
    response = []
    for item in extracted_data:
        response.append({
            "filename": item["filename"],
            "text_preview": item["text"][:500]  # first 500 chars
        })

    return {"status": "success", "files": response}
