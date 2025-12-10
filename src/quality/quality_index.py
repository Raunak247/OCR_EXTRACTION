# src/quality/quality_index.py
from .blur_score import blur_score
from .brightness_score import brightness_score

def compute_quality_index(image_path: str) -> dict:
    b = blur_score(image_path)
    br = brightness_score(image_path)
    # normalize heuristics
    # blur: larger is sharper; scale roughly to 0-1
    blur_norm = min(1.0, b / 1000.0) if b is not None else 0.0
    bright_norm = max(0.0, min(1.0, (br - 50) / 150.0)) if br is not None else 0.0
    overall = round(0.6 * blur_norm + 0.4 * bright_norm, 3)
    return {"overall": overall, "blur": round(blur_norm,3), "brightness": round(bright_norm,3)}

