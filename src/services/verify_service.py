# src/services/verify_service.py
import json
from pathlib import Path
from src.verification.normalizer import normalize_value
from src.verification.similarity import compute_similarity
from src.verification.report_generator import create_report

class VerifyService:
    def verify(self, document_id: str, user_values: dict):
        result_path = Path("files") / document_id / "ocr" / "result.json"
        if not result_path.exists():
            raise FileNotFoundError("No OCR result for document")

        with open(result_path, "r", encoding="utf8") as f:
            extracted = json.load(f)

        field_results = {}
        extracted_fields = extracted.get("fields", {})

        for key, user_val in user_values.items():
            ocr_entry = extracted_fields.get(key)
            if not ocr_entry:
                field_results[key] = {
                    "match": False,
                    "similarity": 0.0,
                    "reason": "field_not_extracted"
                }
                continue

            ocr_text = ocr_entry.get("text") or ""
            norm_ocr = normalize_value(ocr_text)
            norm_user = normalize_value(str(user_val))

            sim = compute_similarity(norm_ocr, norm_user)

            match = sim >= 0.75
            reason = "exact_match" if match else "similarity_below_threshold"

            field_results[key] = {
                "extracted": ocr_text,
                "submitted": user_val,
                "normalized_extracted": norm_ocr,
                "normalized_submitted": norm_user,
                "similarity": round(sim, 3),
                "match": match,
                "reason": reason
            }

        final = create_report(document_id, field_results)
        report_dir = Path("files") / document_id / "report"
        report_dir.mkdir(parents=True, exist_ok=True)
        with open(report_dir / "verification.json", "w", encoding="utf8") as f:
            json.dump(final, f, indent=2, ensure_ascii=False)

        return final
