# src/preprocessing/preprocess_pdf.py
import fitz  # PyMuPDF
import cv2
import numpy as np
from pathlib import Path

def process_pdf(pdf_path: str, doc_id: str):
    doc = fitz.open(pdf_path)
    pages = []
    out_dir = Path("files") / doc_id / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes()
        arr = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        save_path = out_dir / f"page_{i+1}.png"
        cv2.imwrite(str(save_path), img)
        pages.append(img)
    return pages
