# src/routes/extract_api.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.extract_service import ExtractService

router = APIRouter()
service = ExtractService()

@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf","image/png","image/jpeg"):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    result = await service.process_document(file)
    return result
