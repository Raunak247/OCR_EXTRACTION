# OCR_EXTRACTION

# MOSIP OCR & Verification Backend

## Description
A fully local, open-source OCR-driven document extraction and verification backend designed for MOSIP use cases. Complies with all competition requirements. No ML training. No cloud OCR.

## Features
- OCR Extraction API
- Verification API
- Template-driven extraction
- Quality scoring
- Fraud detection (basic)
- MOSIP-aligned digital receipt

## Tech Stack
- Python
- FastAPI
- tryocr / Tesseract
- OpenCV, Pillow
- PDF parsers

## Structure
(Write your folder structure here)

## Setup
pip install -r requirements.txt
uvicorn src.routes.main:app --reload


# OCR Extraction & Verification Backend

## Quick start
1. Install Tesseract OCR and ensure `tesseract` in PATH.
2. python -m venv venv
3. source venv/bin/activate  # or venv\Scripts\activate on Windows
4. pip install -r requirements.txt
5. uvicorn src.main:app --reload --port 8000

## Endpoints
- POST /api/extract (multipart/form-data file, optional template_hint)
- POST /api/verify (json: { "document_id": "...", "user_values": { ... } })
