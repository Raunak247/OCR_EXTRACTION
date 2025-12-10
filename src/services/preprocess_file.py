import os
import uuid
import fitz                     # PyMuPDF
import cv2
import numpy as np
from PIL import Image

def preprocess_file(input_path: str, output_dir: str):
    """
    UNIVERSAL PREPROCESSING:
    - Detect file type (PDF / JPG / PNG)
    - Convert PDF -> images
    - Clean + enhance each image
    - Save inside files/<doc_id>/processed/
    Returns list of processed image paths.
    """

    os.makedirs(output_dir, exist_ok=True)

    ext = os.path.splitext(input_path)[1].lower()

    processed_images = []

    # ---------- PDF HANDLING ----------
    if ext == ".pdf":
        doc = fitz.open(input_path)

        for idx, page in enumerate(doc):
            pix = page.get_pixmap(dpi=200)
            img_path = os.path.join(
                output_dir, f"{uuid.uuid4()}_{idx}.png"
            )
            pix.save(img_path)

            processed = clean_image(img_path)
            processed_images.append(processed)

        return processed_images

    # ---------- IMAGE HANDLING ----------
    else:
        processed = clean_image(input_path)
        processed_images.append(processed)
        return processed_images


def clean_image(image_path: str):
    """
    Enhances image:
    - grayscale
    - noise reduction
    - adaptive threshold
    - deskew-safe
    - saves <original>_clean.png
    """

    img = cv2.imread(image_path)

    if img is None:
        return image_path  # fallback if OpenCV fails

    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # denoise
    denoise = cv2.fastNlMeansDenoising(gray, h=15)

    # threshold
    thr = cv2.adaptiveThreshold(
        denoise, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 8
    )

    # save cleaned version
    clean_path = image_path.replace(".png", "_clean.png")
    cv2.imwrite(clean_path, thr)

    return clean_path
