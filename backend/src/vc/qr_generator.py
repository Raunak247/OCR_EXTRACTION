# src/vc/qr_generator.py
import qrcode
from pathlib import Path

def generate_qr_for_payload(payload: dict, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.make(str(payload))
    qr.save(str(out_path))
    return out_path
