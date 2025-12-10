# src/services/extract_service.py
import asyncio
from pathlib import Path
from src.utils.file_manager import ensure_doc_folder, save_upload_bytes, move_to_processed, save_json
from src.preprocessing.preprocess_file import preprocess_file
from src.ocr.ocr_engine import OCREngine
from src.extraction.field_extractor import extract_fields_from_pages
from src.templates.template_loader import detect_template
from src.utils.logger import get_logger

logger = get_logger("extract_service")

ocr = OCREngine()

class ExtractService:
    async def process_document(self, upload_file):
        """
        upload_file: fastapi UploadFile
        returns result dict and writes files/<doc_id>/ocr/result.json
        """
        data = await upload_file.read()
        # create doc id
        base = ensure_doc_folder()
        doc_id = base.name
        raw_path = save_upload_bytes(doc_id, upload_file.filename, data)

        # preprocess -> processed/<...>
        processed_dir = base / "processed"
        processed_images = preprocess_file(str(raw_path), str(processed_dir))

        # detect template
        template_name = detect_template(processed_images[0]) or "id_card"
        # make crops based on template
        fields = extract_fields_from_pages(processed_images, template_name, base)

        # run OCR on each crop
        for fname, meta in fields.items():
            crop = meta.get("crop_path")
            if not crop:
                fields[fname].update({"text": None, "confidence": 0.0})
                continue
            res = ocr.extract_text(crop)
            fields[fname].update({"text": res.get("text"), "confidence": res.get("confidence"), "engine": res.get("engine")})

        result = {
            "document_id": doc_id,
            "template": template_name,
            "pages": len(processed_images),
            "fields": fields
        }

        save_json(base / "ocr" / "result.json", result)
        logger.info("Extraction done for %s", doc_id)
        return result
