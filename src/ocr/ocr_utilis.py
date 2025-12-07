# src/ocr/ocr_utils.py
import cv2

def read_image_as_gray(path: str):
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Cannot read image: " + path)
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img
