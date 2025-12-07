# src/ocr/tesseract_runner.py
import pytesseract
from PIL import Image
import cv2

def run_tesseract(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        return {"text": "", "confidence": 0.0}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pil = Image.fromarray(gray)
    try:
        text = pytesseract.image_to_string(pil, lang='eng')
        data = pytesseract.image_to_data(pil, output_type=pytesseract.Output.DICT, lang='eng')
        confs = []
        for v in data.get("conf", []):
            try:
                confs.append(float(v))
            except:
                pass
        avg_conf = (sum(confs)/len(confs))/100.0 if confs else 0.0
        return {"text": text.strip(), "confidence": round(avg_conf, 3)}
    except Exception:
        return {"text": "", "confidence": 0.0}
