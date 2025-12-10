# src/preprocessing/preprocess_file.py
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import fitz  # pymupdf
from src.utils.logger import get_logger

logger = get_logger("preprocess")

def _ensure_gray(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def _denoise_and_thresh(img):
    # denoise
    den = cv2.fastNlMeansDenoising(img, None, 15, 7, 21)
    # adaptive threshold
    thr = cv2.adaptiveThreshold(den, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 2)
    return thr

def pdf_to_images(pdf_path: str, out_dir: str):
    doc = fitz.open(pdf_path)
    out = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img_path = Path(out_dir) / f"page_{i+1}.png"
        pix.save(str(img_path))
        out.append(str(img_path))
    return out

def preprocess_file(input_path: str, out_dir: str):
    """
    Universal handler. Returns list of processed image file paths.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ext = Path(input_path).suffix.lower()
    imgs = []
    if ext == ".pdf":
        logger.info("Converting PDF to images")
        imgs = pdf_to_images(input_path, out_dir)
    else:
        imgs = [input_path]

    processed = []
    for p in imgs:
        img = cv2.imread(str(p), cv2.IMREAD_COLOR)
        if img is None:
            logger.warning(f"Could not read image {p}")
            continue
        gray = _ensure_gray(img)
        cleaned = _denoise_and_thresh(gray)
        outp = Path(out_dir) / (Path(p).stem + "_clean.png")
        cv2.imwrite(str(outp), cleaned)
        processed.append(str(outp))
    return processed
