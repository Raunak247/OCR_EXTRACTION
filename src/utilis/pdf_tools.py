# src/utils/pdf_tools.py
from pymupdf import fitz  # pymupdf
import os
from PIL import Image
import io

def pdf_to_images(pdf_path: str, dpi: int = 200):
    doc = fitz.open(pdf_path)
    out_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        data = pix.tobytes()
        img = Image.open(io.BytesIO(data))
        out_path = f"{os.path.splitext(pdf_path)[0]}_page_{i}.png"
        img.save(out_path)
        out_paths.append(out_path)
    return out_paths
