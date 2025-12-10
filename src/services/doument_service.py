# src/services/document_service.py

import json
from pathlib import Path

class DocumentService:
    """
    Yeh class saved OCR results ko file system se read karti hai.
    Iska kaam simple hai: document_id doge → uska OCR JSON de degi.
    """

    def load_extracted_data(self, doc_id: str):
        """
        files/<doc_id>/ocr/result.json ko read karta hai.
        Agar file missing ho to None return karta hai.
        """
        result_path = Path("files") / doc_id / "ocr" / "result.json"

        if not result_path.exists():
            return None

        try:
            with open(result_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
