# src/mosip/qr_generate.py
import qrcode
import os

def generate_qr(payload_json: str, out_path: str):
    img = qrcode.make(payload_json)
    img.save(out_path)
    return out_path
