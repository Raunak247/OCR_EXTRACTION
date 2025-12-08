from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.extract_service import ExtractService

router = APIRouter(tags=["Verification"])
service = ExtractService()

@router.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    """
    Verify user uploaded document by extracting fields.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    result = await service.process_document(file)
    return {
        "status": "success",
        "message": "Document verified",
        "extracted_fields": result
    }
