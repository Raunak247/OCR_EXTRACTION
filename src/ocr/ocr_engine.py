import pytesseract
from PIL import Image
import cv2
import numpy as np


class OCREngine:

    def run_ocr(self, image_path):

        # Load image
        img = cv2.imread(image_path)

        if img is None:
            return "", []

        # Convert to RGB
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Run OCR with bounding boxes
        data = pytesseract.image_to_data(
            rgb,
            output_type=pytesseract.Output.DICT
        )

        extracted_text = " ".join(data["text"])

        # Extract bounding boxes
        boxes = []
        for i in range(len(data["text"])):
            if data["text"][i].strip() != "":
                box = {
                    "text": data["text"][i],
                    "x": data["left"][i],
                    "y": data["top"][i],
                    "w": data["width"][i],
                    "h": data["height"][i],
                }
                boxes.append(box)

        return extracted_text, boxes
