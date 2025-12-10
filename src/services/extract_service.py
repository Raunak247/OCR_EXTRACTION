import uuid
import json
from pathlib import Path
from typing import Optional

from src.utilis.file_manager import create_doc_folders, save_raw_file
from src.preprocessing.preprocess_file import preprocess_file
from src.ocr.ocr_engine import OCREngine
from src.extraction.field_extractor import FieldExtractor
from src.utilis.common import ts

FILES_BASE = Path("files")

class ExtractService:
    def __init__(self):
        self.ocr = OCREngine()
        self.extractor = FieldExtractor()

    async def process_document(self, upload_file, template_hint: Optional[str] = None):
        """
        1. save raw upload to files/<doc_id>/raw/
        2. run preprocess -> get processed image paths
        3. run OCR on each page, aggregate text (and per-zone OCR if template available)
        4. run field extractor to produce structured fields
        5. save files/<doc_id>/ocr/result.json
        """
        doc_id = uuid.uuid4().hex[:8]
        base = create_doc_folders(doc_id)  # returns path str
        base_path = Path(base)

        # Save raw upload
        raw_path = save_raw_file(doc_id, upload_file)  # should write bytes, returns path
        # Preprocess (universal)
        processed_images = preprocess_file(raw_path, output_dir=str(base_path / "processed"))

        # OCR each processed image
        pages_text = []
        fields = {}
        confidences = []
        for img_path in processed_images:
            ocr_res = self.ocr.extract_text_from_image(img_path)
            pages_text.append({"image": str(img_path), "text": ocr_res.get("text",""), "confidence": ocr_res.get("confidence",0)})
            confidences.append(ocr_res.get("confidence", 0))

        # Field extraction (zonal + regex)
        try:
            fields = self.extractor.extract_from_texts([p["text"] for p in pages_text], template_hint=template_hint)
        except Exception:
            # fallback: try extractor on joined text
            joined = "\n".join([p["text"] for p in pages_text])
            fields = self.extractor.extract_from_text(joined)

        quality_score = {
            "average_ocr_confidence": round(sum(confidences)/len(confidences), 2) if confidences else 0.0
        }

        result = {
            "document_id": doc_id,
            "template": template_hint or fields.get("detected_template"),
            "pages": len(processed_images),
            "quality": quality_score,
            "fields": fields,
            "pages_text": pages_text,
            "created_at": ts()
        }

        # Save result JSON
        ocr_dir = base_path / "ocr"
        ocr_dir.mkdir(parents=True, exist_ok=True)
        with open(ocr_dir / "result.json", "w", encoding="utf8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return result
