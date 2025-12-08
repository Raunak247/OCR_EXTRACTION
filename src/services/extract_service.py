# src/services/extract_service.py
import uuid
import os
from fastapi import UploadFile
from src.utilis.file_manager import save_raw_file
from src.preprocessing.preprocess_image import process_image
from src.preprocessing.preprocess_pdf import process_pdf
from src.ocr.ocr_engine import OCREngine
from src.templates.template_loader import TemplateLoader

class ExtractService:

    async def process_document(self, file: UploadFile):
        doc_id = str(uuid.uuid4())

        # 1. Save raw file
        file_path = save_raw_file(doc_id, file)

        # 2. Detect type
        file_ext = file.filename.split(".")[-1].lower()

        if file_ext in ["jpg", "jpeg", "png"]:
            processed_path = process_image(doc_id, file_path)
        elif file_ext == "pdf":
            processed_path = process_pdf(doc_id, file_path)
        else:
            return {"error": "Unsupported file format"}

        # 3. OCR
        ocr = OCREngine()
        raw_text, boxes = ocr.run_ocr(processed_path)

        # 4. Template matching
        template_service = TemplateLoader()
        fields = template_service.extract_fields(doc_id, boxes, processed_path)

        # 5. Response
        return {
            "doc_id": doc_id,
            "raw_text": raw_text,
            "fields": fields,
            "status": "success"
        }
