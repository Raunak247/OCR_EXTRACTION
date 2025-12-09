# src/vc/qr_generator.p
import qrcode
from PIL import Image

def generate_qr(data: dict, out_path: str):
    """
    Encode minimal VC reference (or full VC) into QR code PNG.
    """
    payload = str(data)  # for demo; in prod use compact UID / URL to VC
    img = qrcode.make(payload)
    img = img.convert("RGB")
    img.save(out_path)
    return out_path
