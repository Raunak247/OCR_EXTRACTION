# src/quality/quality_index.py
import cv2
from .blur_score import blur_score
from .brightness_score import brightness_score

def compute_quality_score(img):
    if img is None:
        return {"overall": 0.0, "blur": 0.0, "brightness": 0.0}
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    blur = blur_score(gray)
    bright = brightness_score(gray)
    overall = round(0.6 * blur + 0.4 * bright, 3)
    return {"overall": overall, "blur": round(blur, 3), "brightness": round(bright, 3)}
