import json
import os


class TemplateLoader:

    def __init__(self, template_dir="src/templates"):
        self.template_dir = template_dir

    def load_template(self, template_name):
        path = os.path.join(self.template_dir, template_name)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Template not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

