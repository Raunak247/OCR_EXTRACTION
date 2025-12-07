# src/ocr/ocr_engine.py
from src.ocr.tryocr_runner import run_tryocr
from src.ocr.tesseract_runner import run_tesseract

def run_ocr_on_image_path(image_path: str):
    # First try optional tryocr (if implemented), fallback to tesseract
    res = run_tryocr(image_path)
    if not res or res.get("confidence", 0.0) < 0.4:
        res = run_tesseract(image_path)
    return res
