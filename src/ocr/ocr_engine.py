# src/ocr/ocr_engine.py
import os
from PIL import Image
import pytesseract
from src.utilis.loggers import get_logger

logger = get_logger("ocr_engine")

# try TrOCR via transformers if available
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    import torch
    HAS_TROCR = True
except Exception:
    HAS_TROCR = False

class OCREngine:
    def __init__(self, lang: str = "eng"):
        self.lang = lang
        if HAS_TROCR:
            try:
                self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
                self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
                logger.info("TrOCR loaded")
            except Exception as e:
                logger.warning("TrOCR load failed: %s", e)
                self.processor = None
                self.model = None
        else:
            self.processor = None
            self.model = None

    def extract_text_tesseract(self, image_path: str):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang=self.lang)
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=self.lang)
            confs = []
            for c in data.get("conf", []):
                try:
                    v = float(c)
                    if v >= 0:
                        confs.append(v)
                except:
                    pass
            avg = round(sum(confs)/len(confs), 2) if confs else 0.0
            return {"text": text.strip(), "confidence": avg, "engine": "tesseract"}
        except Exception as e:
            logger.exception("Tesseract failed")
            return {"text": "", "confidence": 0.0, "engine": "tesseract", "error": str(e)}

    def extract_text_trocr(self, image_path: str):
        if not HAS_TROCR or self.processor is None:
            return {"text": "", "confidence": 0.0, "engine": "trocr", "error": "not available"}
        try:
            img = Image.open(image_path).convert("RGB")
            pixel_values = self.processor(images=img, return_tensors="pt").pixel_values
            ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(ids, skip_special_tokens=True)[0]
            return {"text": text.strip(), "confidence": 85.0, "engine": "trocr"}
        except Exception as e:
            logger.exception("TrOCR failed")
            return {"text": "", "confidence": 0.0, "engine": "trocr", "error": str(e)}

    def extract_text(self, image_path: str):
        res = self.extract_text_tesseract(image_path)
        if res.get("confidence", 0) < 40 and HAS_TROCR:
            logger.info("Low confidence from Tesseract (%s). Trying TrOCR", res.get("confidence"))
            tro = self.extract_text_trocr(image_path)
            # choose longer output or higher confidence
            if len(tro["text"]) > len(res["text"]) or tro.get("confidence",0) > res.get("confidence",0):
                return tro
        return res
