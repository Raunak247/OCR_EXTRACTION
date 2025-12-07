# src/templates/template_loader.py
import json
from pathlib import Path

TEMPLATE_DIR = Path("src") / "templates"

def load_template(name: str):
    p = TEMPLATE_DIR / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError("Template not found: " + name)
    return json.loads(p.read_text(encoding="utf8"))

def detect_template(image):
    # Basic heuristic: image shape or visual anchor detection can be added.
    # For now default to id_card
    return "id_card"
