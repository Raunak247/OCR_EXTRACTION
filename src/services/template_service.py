# src/services/template_service.py

from src.templates.template_loader import load_template

class TemplateService:
    """
    Yeh class responsible hai template JSON files ko load karne ke liye.
    Har document type ke liye alag template hota hai (id_card, form, certificate).
    """

    def get_template(self, template_name: str):
        """
        Template ka naam doge → uska JSON return karega.
        """
        try:
            return load_template(template_name)
        except FileNotFoundError:
            raise FileNotFoundError(f"Template '{template_name}' nahi mila.")

    def get_default_template(self):
        """
        Default template koi bhi ho sakta hai (safe fallback).
        Yaha hum id_card rakh rahe hain.
        """
        return load_template("id_card")
