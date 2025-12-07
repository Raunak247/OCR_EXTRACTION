# src/preprocessing/brightness_contrast.py
import cv2

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    # brightness: -100..100, contrast: -100..100
    if brightness != 0:
        beta = brightness
    else:
        beta = 0
    if contrast != 0:
        alpha = 1 + contrast / 100.0
    else:
        alpha = 1.0
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
