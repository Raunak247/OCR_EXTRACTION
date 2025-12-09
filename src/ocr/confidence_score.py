# src/ocr/confidence_score.py
import pytesseract
from PIL import Image
import numpy as np

def avg_confidence_from_image(image_path: str) -> float:
    """
    Use pytesseract.image_to_data to compute average confidence (0-100).
    Returns 0-100 float.
    """
    try:
        data = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
        confs = []
        for c in data.get("conf", []):
            try:
                v = float(c)
                if v >= 0:
                    confs.append(v)
            except Exception:
                continue
        if not confs:
            return 0.0
        return round(sum(confs) / len(confs), 2)
    except Exception:
        return 0.0
