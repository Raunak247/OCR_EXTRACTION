# src/services/extract_service.py
import uuid
import json
from pathlib import Path

from src.utils.file_manager import create_doc_folders, save_raw_file
from src.preprocessing.preprocess_pdf import process_pdf
from src.preprocessing.preprocess_image import process_image
from src.templates.template_loader import detect_template, load_template
from src.ocr.ocr_engine import run_ocr_on_image_path
from src.quality.quality_index import compute_quality_score

class ExtractService:
    async def process_document(self, upload_file, template_hint=None):
        doc_id = uuid.uuid4().hex[:8]
        base = create_doc_folders(doc_id)

        raw_path = await save_raw_file(doc_id, upload_file)

        pages = []
        if raw_path.lower().endswith(".pdf"):
            pages = process_pdf(raw_path, doc_id)
        else:
            img = process_image(raw_path, doc_id)
            pages = [img]

        template_name = template_hint or detect_template(pages[0])
        template = load_template(template_name)

        fields_out = {}
        crops_dir = Path(base) / "crops"
        crops_dir.mkdir(parents=True, exist_ok=True)

        for field_name, cfg in template.items():
            page_idx = max(0, cfg.get("page", 1) - 1)
            if page_idx >= len(pages):
                fields_out[field_name] = {"text": None, "confidence": 0.0, "note": "page_missing"}
                continue

            x1, y1, x2, y2 = cfg["box"]
            page_img = pages[page_idx]
            h, w = page_img.shape[:2]
            x1c, y1c = max(0, x1), max(0, y1)
            x2c, y2c = min(w, x2), min(h, y2)
            if x1c >= x2c or y1c >= y2c:
                fields_out[field_name] = {"text": None, "confidence": 0.0, "note": "invalid_box"}
                continue
            crop = page_img[y1c:y2c, x1c:x2c]

            crop_path = str(crops_dir / f"{field_name}.png")
            import cv2
            cv2.imwrite(crop_path, crop)

            ocr_res = run_ocr_on_image_path(crop_path)
            fields_out[field_name] = ocr_res

        quality = compute_quality_score(pages[0])

        result = {
            "document_id": doc_id,
            "template": template_name,
            "pages": len(pages),
            "quality": quality,
            "fields": fields_out
        }

        Path(base, "ocr").mkdir(parents=True, exist_ok=True)
        with open(Path(base) / "ocr" / "result.json", "w", encoding="utf8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return result
