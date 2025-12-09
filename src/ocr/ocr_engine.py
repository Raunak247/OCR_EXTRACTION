# src/ocr/ocr_engine.py
import os
from typing import Optional
from PIL import Image
import pytesseract
import torch
import transformers

# Try loading TrOCR (HuggingFace version, NOT 'tryocr')
# Try loading TrOCR (HuggingFace version, NOT 'tryocr')
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    import torch
    HAS_TRYOCR = True
except Exception:
    HAS_TRYOCR = False



class OCREngine:
    """
    Unified OCR engine wrapper.
    - Primary: pytesseract (offline, stable)
    - Optional: Microsoft TrOCR (if installed)
    """

    def __init__(self, lang: str = "eng"):
        self.lang = lang

        # Initialize TrOCR only if available
        if HAS_TROCR:
            try:
                self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
                self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
                print("🔵 TrOCR loaded successfully.")
            except Exception:
                self.processor = None
                self.model = None
                print("⚠️ TrOCR import found but failed to initialize.")
        else:
            self.processor = None
            self.model = None
            print("🟡 TrOCR not installed — using Tesseract only.")


    # ---------------------------------------------------------
    # Tesseract extraction
    # ---------------------------------------------------------
    def extract_text_tesseract(self, image_path: str) -> dict:
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang=self.lang)

            # Confidence extraction
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=self.lang)
            confs = [
                float(c) for c in data.get("conf", []) 
                if c not in ["-1", "", None]
            ]

            avg_conf = round(sum(confs) / len(confs), 2) if confs else 0.0

            return {"text": text.strip(), "confidence": avg_conf, "engine": "tesseract"}

        except Exception as e:
            return {"text": "", "confidence": 0.0, "engine": "tesseract", "error": str(e)}


    # ---------------------------------------------------------
    # TrOCR extraction (optional)
    # ---------------------------------------------------------
    def extract_text_trocr(self, image_path: str) -> dict:
        if not HAS_TROCR or self.processor is None:
            return {"text": "", "confidence": 0.0, "engine": "trocr", "error": "TrOCR not available"}

        try:
            img = Image.open(image_path).convert("RGB")

            pixel_values = self.processor(images=img, return_tensors="pt").pixel_values
            ids = self.model.generate(pixel_values)
            text = self.processor.batch_decode(ids, skip_special_tokens=True)[0]

            # TrOCR has no confidence calculation → set placeholder
            return {"text": text.strip(), "confidence": 90.0, "engine": "trocr"}

        except Exception as e:
            return {"text": "", "confidence": 0.0, "engine": "trocr", "error": str(e)}


    # ---------------------------------------------------------
    # Auto engine selector
    # ---------------------------------------------------------
    def extract_text_from_image(self, image_path: str) -> dict:

        # 1) Try Tesseract first
        result = self.extract_text_tesseract(image_path)

        # If Tesseract fails or confidence is too low → try TrOCR
        if result["confidence"] < 50 and HAS_TROCR:
            print("⚠ Low confidence — switching to TrOCR…")
            trocr_result = self.extract_text_trocr(image_path)

            # if TrOCR gives better text, use it
            if len(trocr_result["text"]) > len(result["text"]):
                return trocr_result

        return result


    # ---------------------------------------------------------
    # Byte input (from uploads)
    # ---------------------------------------------------------
    def extract_text_from_bytes(self, b: bytes) -> dict:
        import tempfile
        p = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        p.write(b)
        p.flush()
        p.close()

        res = self.extract_text_from_image(p.name)

        try:
            os.unlink(p.name)
        except:
            pass

        return res
