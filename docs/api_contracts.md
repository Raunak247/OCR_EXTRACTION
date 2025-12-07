# OCR Extraction & Verification System — Architecture

## 1. Overview
Yeh system do core kaam karta hai:
1. Document se fields extract karna (OCR)
2. Extracted fields ko user-submitted data se verify karna

Pure solution local machine par chalne layak hai, bina cloud services ka use kiye.

---

## 2. High-Level Flow

1. User document upload karta hai (image ya PDF)
2. System file ko `/files/<doc_id>/raw/` me store karta hai
3. Preprocessing hota hai (deskew, noise removal, brightness fix)
4. Template load hota hai → zones detect hote hain
5. OCR run hota hai har zone par
6. Fields as JSON return hote hain
7. Verification API extracted data aur user form data ko compare karti hai
8. Report generate hoti hai (match/mismatch + score)

---

## 3. Core Modules

### **a) Preprocessing**
- Deskew  
- Noise removal  
- Brightness/contrast correction  
- PDF page conversion  
- Cropping zones  

### **b) Template Engine**
Har document type ke liye:
- JSON template hota hai  
- Usme OCR zones defined hote hain  
- Template detect + zone extraction hota hai  

### **c) OCR Layer**
System me do engines:
- tryOCR (primary)
- Tesseract (fallback)

### **d) Verification Engine**
- Field-wise comparison  
- Similarity score  
- Match/Partial/Mismatch  
- Reasoning include  

### **e) Quality Scoring**
- Blur detection  
- Brightness issues  
- Skew detection  
- Quality Index = weighted score  

### **f) Fraud/Tamper Checks**
(Heuristic-based)
- Noise pattern changes  
- Lighting anomalies  
- Patch detection  

---

## 4. Directory Structure (Short Summary)

src/
preprocessing/
ocr/
services/
verification/
templates/
quality/
fraud/
routes/


---

## 5. API Layer (FastAPI)
- extract_api.py → Extraction endpoint  
- verify_api.py → Verification endpoint  
- health_api.py → Health status  

---

## 6. Data Flow Diagram (Simplified)

Upload → Preprocess → Template Zones → OCR → Extracted JSON
↓
Verification (User Data)
↓
Final Report


---

## 7. Why This Architecture?
- PS ke according tamamen local computation
- MOSIP workflows ke saath easily integrate ho sakta hai
- Modular design → har part independent testable
- Cloud-independent open-source tech stack
