# src/preprocessing/preprocess_image.py
import cv2
from pathlib import Path

def process_image(img_path: str, doc_id: str):
    img = cv2.imread(img_path)
    if img is None:
        raise RuntimeError("Could not read image")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    target_w = 1200
    if w != target_w:
        scale = target_w / w
        gray = cv2.resize(gray, (target_w, int(h * scale)))
    out_path = Path("files") / doc_id / "processed" / "page_1.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), gray)
    return gray
