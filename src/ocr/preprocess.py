# src/ocr/preprocess.py
import os
import shutil
from typing import List
from src.utilis.image_tools import read_image, to_grayscale, denoise, threshold, save_image
from src.utilis.pdf_tools import pdf_to_images
from src.utilis.loggers import logger

def preprocess_file(path: str, output_dir: str):
    
    # return list of processed images

    os.makedirs(output_dir, exist_ok=True)
    ext = os.path.splitext(input_path)[1].lower()
    images = []
    if ext == ".pdf":
        logger.info("Converting PDF to images: %s", input_path)
        pages = pdf_to_images(input_path, dpi=200)
        for p in pages:
            dst = os.path.join(output_dir, os.path.basename(p))
            # basic processing
            img = read_image(p)
            if img is None:
                continue
            gray = to_grayscale(img)
            thr = threshold(gray)
            save_image(dst, thr)
            images.append(dst)
            try:
                os.remove(p)
            except Exception:
                pass
        return images
    else:
        img = read_image(input_path)
        if img is None:
            return []
        # denoise -> grayscale -> threshold
        img = denoise(img)
        gray = to_grayscale(img)
        thr = threshold(gray)
        out_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + "_proc.png")
        save_image(out_path, thr)
        images.append(out_path)
        return images
