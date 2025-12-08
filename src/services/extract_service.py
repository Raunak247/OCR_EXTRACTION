import uuid
import os
from fastapi import UploadFile
from src.preprocessing.preprocess_pdf import process_pdf

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ExtractService:

    async def process_document(self, file: UploadFile):
        # Generate unique file path with extension
        doc_id = str(uuid.uuid4())
        file_ext = file.filename.split(".")[-1]
        saved_path = os.path.join(UPLOAD_DIR, f"{doc_id}.{file_ext}")

        # Save uploaded file
        with open(saved_path, "wb") as f:
            f.write(await file.read())

        # Process PDF
        try:
            processed_path = process_pdf(saved_path)
        except Exception as e:
            return {"error": f"Processing error: {str(e)}"}

        return {
            "doc_id": doc_id,
            "uploaded_file": saved_path,
            "processed_file": processed_path
        }
