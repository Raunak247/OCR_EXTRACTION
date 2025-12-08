from fastapi import APIRouter, UploadFile, File
from src.services.extract_service import ExtractService

router = APIRouter(prefix="/api", tags=["Extraction"])

@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    service = ExtractService()
    result = await service.process_document(file)
    return result
