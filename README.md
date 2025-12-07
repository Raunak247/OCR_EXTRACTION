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
