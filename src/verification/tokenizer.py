import re

class TextTokenizer:
    def __init__(self):
        # Common cleanup patterns
        self.patterns = [
            (r"\n+", " "),          # remove extra newlines
            (r"\s{2,}", " "),       # remove multiple spaces
            (r"[^a-zA-Z0-9.,:%\-\/ ]", ""),  # remove symbols
        ]

    def clean(self, text: str) -> str:
        text = text.strip()
        for pattern, repl in self.patterns:
            text = re.sub(pattern, repl, text)
        return text

    def tokenize(self, text: str):
        text = self.clean(text)
        return text.split(" ")
