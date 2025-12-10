# src/extraction/field_extractor.py
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
from src.templates.template_loader import load_template
from src.utils.logger import get_logger

logger = get_logger("field_extractor")

def crop_field(page_img_path: str, box):
    img = cv2.imread(page_img_path)
    h, w = img.shape[:2]
    x1, y1, x2, y2 = box
    # clamp
    x1, y1 = max(0,int(x1)), max(0,int(y1))
    x2, y2 = min(w,int(x2)), min(h,int(y2))
    crop = img[y1:y2, x1:x2]
    return crop

def extract_fields_from_pages(processed_pages: list, template_name: str, doc_base: Path):
    """
    processed_pages: list of file paths (strings) for pages
    template: JSON mapping field->{page, box}
    """
    tpl = load_template(template_name)
    out = {}
    crops_dir = doc_base / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    for field_name, cfg in tpl.items():
        page_idx = max(0, cfg.get("page",1)-1)
        if page_idx >= len(processed_pages):
            out[field_name] = {"text": None, "note":"page_missing", "confidence":0}
            continue
        page_path = processed_pages[page_idx]
        box = cfg.get("box", [0,0,0,0])
        crop_img = crop_field(page_path, box)
        crop_path = crops_dir / f"{field_name}.png"
        cv2.imwrite(str(crop_path), crop_img)
        out[field_name] = {"crop_path": str(crop_path)}
    return out
