# src/templates/template_loader.py
import json
from pathlib import Path
from typing import Optional
from PIL import Image

TEMPLATE_DIR = Path("src") / "templates"

def load_template(name: str) -> dict:
    p = TEMPLATE_DIR / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError(f"Template not found: {name}")
    return json.loads(p.read_text(encoding="utf8"))

def detect_template(image_path: str) -> Optional[str]:
    """
    Very simple detection: you can expand this by checking sizes or keywords in OCR.
    For now returns 'id_card' if file exists else None.
    """
    # Simple heuristic: check width/height of first image
    try:
        img = Image.open(image_path)
        w, h = img.size
        # fallback mapping (tunable)
        if w <= 800 and h <= 600:
            return "id_card"
        return "form"
    except Exception:
        return None

