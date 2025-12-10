# src/ocr/trocr_engine.py
"""
TrOCR wrapper using HuggingFace transformers (optional).
If not installed, the module will raise ImportError when imported.
"""
from typing import List
from PIL import Image
import torch

from transformers import TrOCRProcessor, VisionEncoderDecoderModel

class TrOCREngine:
    def __init__(self, model_name="microsoft/trocr-base-printed", device=None):
        self.model_name = model_name
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = TrOCRProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def ocr_image(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        pixel_values = self.processor(image, return_tensors="pt").pixel_values.to(self.device)
        generated_ids = self.model.generate(pixel_values, max_length=256)
        preds = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
        return preds[0].strip()

    def ocr_batch(self, image_paths: List[str]) -> str:
        texts = []
        for p in image_paths:
            texts.append(self.ocr_image(p))
        return "\n".join(texts)
