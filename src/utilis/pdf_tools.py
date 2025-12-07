# src/utils/pdf_tools.py

import fitz  # PyMuPDF
from pathlib import Path
import cv2
import numpy as np


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 300):
    """
    Convert PDF pages into PNG images.

    Args:
        pdf_path (str): path to input PDF file
        output_dir (str): destination directory where page_<num>.png will be saved
        dpi (int): output DPI for better OCR clarity

    Returns:
        List of numpy image arrays (OpenCV format)
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    images = []

    for idx, page in enumerate(doc):
        # Render page into bitmap
        pix = page.get_pixmap(dpi=dpi)

        # Convert pixmap bytes to numpy image
        img_bytes = pix.tobytes("png")
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError(f"Unable to decode PDF page {idx + 1}")

        # Save image to disk
        save_path = Path(output_dir) / f"page_{idx + 1}.png"
        cv2.imwrite(str(save_path), img)

        images.append(img)

    return images


def get_pdf_page_count(pdf_path: str):
    """
    Returns total number of pages inside PDF.

    Args:
        pdf_path (str): path to PDF file

    Returns:
        int: number of pages
    """
    try:
        doc = fitz.open(pdf_path)
        return len(doc)
    except Exception:
        return 0
