# src/templates/template_loader.py
import json
from pathlib import Path

TEMPLATE_DIR = Path("src/templates")

def load_template(name: str):
    p = TEMPLATE_DIR / f"{name}.json"
    if not p.exists():
        raise FileNotFoundError(f"Template {name} not found")
    return json.loads(p.read_text(encoding="utf8"))

def detect_template(image_path: str):
    # simple default detection — can be improved
    # for now return "id_card" if exists else first template
    if (TEMPLATE_DIR / "id_card.json").exists():
        return "id_card"
    files = list(TEMPLATE_DIR.glob("*.json"))
    return files[0].stem if files else None
