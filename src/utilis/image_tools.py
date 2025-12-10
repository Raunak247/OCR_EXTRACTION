# src/utils/image_tools.py
import cv2
import numpy as np
import os
from PIL import Image

def read_image(path: str):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

def save_image(path: str, img):
    # cv2.imwrite can't handle unicode path on Windows reliably - use imencode and write binary
    ext = os.path.splitext(path)[1]
    success, buf = cv2.imencode(ext, img)
    if not success:
        raise RuntimeError("Failed to encode image")
    with open(path, "wb") as f:
        f.write(buf.tobytes())

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

def threshold(img_gray):
    return cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 2)
