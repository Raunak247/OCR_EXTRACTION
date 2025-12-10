# API Contracts (Extraction + Verification)

## 1. Extraction API
### **POST /extract**
Document se text fields extract karta hai.

### Request
**Content-Type:** multipart/form-data

file: <uploaded file>
doc_type: "id_card" | "form" | "certificate"


### Response (Example)
```json
{
  "doc_id": "A23F9D",
  "doc_type": "id_card",
  "quality": {
    "blur": 0.82,
    "brightness": 0.76,
    "skew": 0.91,
    "quality_index": 0.83
  },
  "extracted_fields": {
    "name": "Raunak Pantawane",
    "dob": "12-05-2001",
    "id_number": "XYZ12345"
  }
}


2. Verification API
POST /verify
Input

{
  "doc_id": "A23F9D",
  "submitted_fields": {
    "name": "Raunak Pantawane",
    "dob": "12/05/2001",
    "id_number": "XYZ12345"
  }
}
# output

{
  "verification_result": {
    "name": {
      "extracted_value": "Raunak Pantawane",
      "submitted_value": "Raunak Pantawane",
      "score": 0.96,
      "status": "match",
      "reason": "Values are highly similar"
    },
    "dob": {
      "extracted_value": "12-05-2001",
      "submitted_value": "12/05/2001",
      "score": 0.72,
      "status": "partial_match",
      "reason": "Formatting difference"
    }
  }
}
3. Health API
GET /health

{
  "status": "running",
  "ocr_engine": "tryocr"
}


---

# ✅ **3) docs/ps_mapping.md**

```markdown
# Problem Statement Mapping → Our Solution

## 1. Mandatory Task Mapping

| PS Requirement | Our Implementation |
|----------------|-------------------|
| OCR extraction | tryOCR + Tesseract runners |
| Form autofill | Template-based field mapping |
| Verification API | compare_fields + normalizer |
| Local-only solution | No cloud usage |
| Handles ID cards, forms, certificates | templates/id_card.json, form.json, certificate.json |

---

## 2. Good-To-Have Mapping

| Requirement | Status |
|------------|--------|
| Multi-language | Easily extendable |
| Handwriting support | Partial (engine supports basic) |
| Manual correction | Frontend side ready |
| Multi-page PDF | preprocess_pdf.py supports |

---

## 3. Bonus Task Mapping (MOSIP Focused)

| Bonus Task | Implementation |
|------------|----------------|
| Capture Quality | blur_score, brightness_score, skew_score |
| Fraud detection | noise_pattern_check, patch_analysis |
| MOSIP integration | Architecture aligned (Registration pipeline-compatible) |

---

## 4. Tech Stack Mapping

| Mentioned in PS | Used |
|------------------|------|
| OCR tools | tryOCR / Tesseract |
| Local processing | Yes |
| Open-source | 100% open-source modules |

---

## 5. Why This Solution Fits MOSIP?
- Field extraction + verification = MOSIP registration flow ka core
- Capture-quality is a MOSIP requirement
- Works offline (MOSIP’s on-site capture rule)
- Supports template-based Indian documents
