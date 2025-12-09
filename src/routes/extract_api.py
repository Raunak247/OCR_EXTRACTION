from fastapi import APIRouter, UploadFile, File
from PIL import Image
import pytesseract
import io

router = APIRouter()

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # OCR
        text = pytesseract.image_to_string(image)

        return {"status": "success", "text": text}

    except Exception as e:
        return {"status": "error", "message": str(e)}
