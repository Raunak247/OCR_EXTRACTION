# Setup Guide — OCR Extraction & Verification System

## 1. System Requirements
- Python 3.9+
- pip
- Tesseract OCR installed
- Local machine (no cloud required)

---

## 2. Install Dependencies
Terminal me run karein:

## pip install -r requirements.txt


Ensure tesseract installed:

**Windows:**
Install from: https://github.com/UB-Mannheim/tesseract/wiki

Path add karein:

## C:\Program Files\Tesseract-OCR


---

## 3. Project Initialization


Create folders automatically created at runtime:

---

## 4. Run FastAPI Server


Server open karein:

---

## 5. Testing Extraction
API → `/extract`

Upload:
- sample_docs/id_card.jpg
- sample_docs/certificate.png
- sample_docs/form.pdf

---

## 6. Testing Verification
Use:
- doc_id from extraction  
- Submit fields via JSON body  

---

## 7. Troubleshooting

| Error | Solution |
|-------|----------|
| OCR blank | Increase brightness, check resolution |
| Tesseract not found | Add it to PATH |
| PDF not converting | Install Poppler |

---

## 8. Deployment Notes
- Runs fully offline  
- No license restrictions  
- Can run inside MOSIP enrollment kits  


