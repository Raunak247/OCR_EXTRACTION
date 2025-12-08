from fastapi import APIRouter, UploadFile, File
from src.services.extract_service import ExtractService

router = APIRouter(prefix="/api", tags=["Extraction"])
service = ExtractService()

@router.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    return await service.process_document(file)
