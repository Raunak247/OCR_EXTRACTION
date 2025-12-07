# src/preprocessing/noise_removal.py
import cv2

def denoise(image):
    return cv2.fastNlMeansDenoising(image, None, 15, 7, 21)
