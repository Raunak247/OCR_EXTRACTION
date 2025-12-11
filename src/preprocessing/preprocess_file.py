# src/preprocessing/preprocess_file.py
import os
import uuid
import fitz              # PyMuPDF
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from src.utilis.common import ensure_dir  # using your 'utilis' folder

def _clean_image_cv(in_path: str, out_path: str):
    """Read image, apply denoise/deskew/threshold and save to out_path."""
    img = cv2.imread(in_path, cv2.IMREAD_COLOR)
    if img is None:
        # fallback: try PIL
        try:
            pil = Image.open(in_path).convert("RGB")
            pil.save(out_path)
            return out_path
        except Exception:
            return in_path

    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # denoise
    den = cv2.fastNlMeansDenoising(gray, None, 15, 7, 21)

    # adaptive threshold (helps OCR)
    thr = cv2.adaptiveThreshold(den, 255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 31, 2)

    # optional resize if too small
    h, w = thr.shape[:2]
    target_w = 1200
    if w < target_w:
        scale = target_w / w
        thr = cv2.resize(thr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_LINEAR)

    # save
    cv2.imwrite(out_path, thr)
    return out_path


def preprocess_file(input_path: str, output_dir: str = None):
    """
    Universal handler:
      - input_path: path to an uploaded file (pdf or image)
      - output_dir: directory where processed images will be saved (created if needed)
    Returns: list of processed image file paths (PNG)
    """
    if not output_dir:
        output_dir = str(Path("processed"))
    ensure_dir(output_dir)

    ext = Path(input_path).suffix.lower()
    out_paths = []

    # PDF -> convert pages to PNG using PyMuPDF
    if ext == ".pdf":
        try:
            doc = fitz.open(input_path)
        except Exception:
            return out_paths
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)
            tmp_name = f"{uuid.uuid4().hex}_page{i+1}.png"
            tmp_path = str(Path(output_dir) / tmp_name)
            pix.save(tmp_path)
            # clean the generated image and overwrite to cleaned version
            cleaned = tmp_path.replace(".png", "_clean.png")
            _clean_image_cv(tmp_path, cleaned)
            out_paths.append(cleaned)
        return out_paths

    # Image files
    else:
        # accept jpg/png/jpeg, gif etc.
        in_name = Path(input_path).name
        out_name = f"{uuid.uuid4().hex}_{in_name}"
        out_path = str(Path(output_dir) / out_name)
        # copy original first (PIL) then clean
        try:
            img = Image.open(input_path).convert("RGB")
            img.save(out_path)
        except Exception:
            # if saving fails, just try to run clean on original
            out_path = input_path

        cleaned = str(Path(output_dir) / (Path(out_path).stem + "_clean.png"))
        _clean_image_cv(out_path, cleaned)
        out_paths.append(cleaned)
        return out_paths
def get_logger():
    from src.utilis.loggers import get_logger
    return get_logger()
logger = get_logger()
