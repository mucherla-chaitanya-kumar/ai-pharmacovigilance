FROM python:3.10-slim

WORKDIR /app

# System deps (PDF + OCR)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install spaCy models explicitly
RUN python -m spacy download en_core_web_sm && \
    python -m spacy download en_core_sci_sm

# Copy app code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.mainf:app", "--host", "0.0.0.0", "--port", "8000"]
