# src/ocr/extractor.py
import os
from typing import List, Dict
from src.utilis.loggers import logger

# Try to import trOCR
HAS_TROCR = False
try:
    from src.ocr.trocr_engine import TrOCREngine
    HAS_TROCR = True
except Exception:
    HAS_TROCR = False

# fallback to pytesseract
try:
    import pytesseract
    from PIL import Image
    HAS_PYTESSACT = True
except Exception:
    HAS_PYTESSACT = False

class OCREngineWrapper:
    def __init__(self, trocr_model_name: str = None):
        self.trocr = None
        if HAS_TROCR and trocr_model_name:
            try:
                self.trocr = TrOCREngine(model_name=trocr_model_name)
                logger.info("TrOCR engine loaded")
            except Exception as e:
                logger.warning("Failed to init TrOCR: %s", e)
                self.trocr = None

    def extract_from_images(self, image_paths: List[str]) -> Dict:
        """
        Returns {"text": "...", "engine": "trocr"|"pytesseract", "blocks": [...]}
        """
        if self.trocr:
            try:
                txt = self.trocr.ocr_batch(image_paths)
                return {"text": txt, "engine": "trocr"}
            except Exception as e:
                logger.warning("TrOCR error: %s", e)

        # fallback
        if HAS_PYTESSACT:
            texts = []
            for p in image_paths:
                try:
                    img = Image.open(p)
                    t = pytesseract.image_to_string(img, lang="eng")
                    texts.append(t)
                except Exception as e:
                    logger.exception("pytesseract failed for %s: %s", p, e)
            return {"text": "\n".join(texts), "engine": "pytesseract"}
        else:
            return {"text": "", "engine": "none", "error": "No OCR engine installed"}
