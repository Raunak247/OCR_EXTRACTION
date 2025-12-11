import json
from pathlib import Path
from src.verification.compare_fields import compare
from src.verification.accuracy_score import compute_overall_score
from src.mosip.vc_issuer import VCIssuer
from src.utilis.file_manager import ensure_doc_folder
from src.utilis.common import ts

FILES_BASE = Path("files")

class VerifyService:
    def __init__(self, vc_auto_issue_threshold: int = 85):
        self.vc_issuer = VCIssuer()
        self.vc_auto_issue_threshold = vc_auto_issue_threshold

    def verify(self, document_id: str, user_values: dict) -> dict:
        """
        document_id: id returned by extract endpoint
        user_values: dict of user-submitted fields (strings)
        """
        result_path = FILES_BASE / document_id / "ocr" / "result.json"
        if not result_path.exists():
            raise FileNotFoundError(f"No OCR result for document {document_id}")

        with open(result_path, "r", encoding="utf8") as f:
            extracted = json.load(f)

        extracted_fields = extracted.get("fields", {})

        per_field = {}
        for key, user_val in user_values.items():
            extracted_val = extracted_fields.get(key)
            if extracted_val is None:
                # field not extracted
                per_field[key] = {
                    "extracted": None,
                    "submitted": user_val,
                    "similarity": 0.0,
                    "match": False,
                    "reason": "field_not_extracted"
                }
                continue

            cmp = compare(extracted_val, user_val)
            per_field[key] = cmp

        overall = compute_overall_score(per_field)

        report = {
            "document_id": document_id,
            "timestamp": ts(),
            "overall_score": overall,
            "fields": per_field
        }

        # Save verification report
        ver_dir = FILES_BASE / document_id / "verification"
        ver_dir.mkdir(parents=True, exist_ok=True)
        with open(ver_dir / "verification.json", "w", encoding="utf8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # If good enough automatically issue VC and save in report folder
        if overall >= self.vc_auto_issue_threshold:
            subject = {
                "name": user_values.get("name", extracted_fields.get("name")),
                "dob": user_values.get("dob", extracted_fields.get("dob")),
                "address": user_values.get("address", extracted_fields.get("address")),
                "docType": extracted.get("template", "unknown"),
                "docNumber": user_values.get("id_number", extracted_fields.get("id_number")),
                "score": overall
            }
            vc_res = self.vc_issuer.issue_vc(subject)
            report["vc"] = vc_res

            # save VC into report folder
            report_dir = FILES_BASE / document_id / "report"
            report_dir.mkdir(parents=True, exist_ok=True)
            with open(report_dir / f"{vc_res['vc_id']}.json", "w", encoding="utf8") as f:
                json.dump(vc_res, f, indent=2, ensure_ascii=False)

        return report
