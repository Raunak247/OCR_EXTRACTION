# src/quality/blur_score.py
import cv2

def blur_score(image):
    val = cv2.Laplacian(image, cv2.CV_64F).var()
    return min(1.0, val / 1000)
