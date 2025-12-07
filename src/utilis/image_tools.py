# src/utils/image_tools.py
import cv2

def to_gray(image):
    """Convert BGR image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_keep_ratio(image, width=1200):
    """Resize while maintaining aspect ratio."""
    h, w = image.shape[:2]
    if w == width:
        return image
    scale = width / w
    new_h = int(h * scale)
    return cv2.resize(image, (width, new_h))

def load_image(path):
    """Load an image safely."""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not load image: {path}")
    return img
