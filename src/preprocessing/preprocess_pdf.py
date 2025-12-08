import fitz
import os

OUTPUT_DIR = "processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    text_output = ""

    for page in doc:
        text_output += page.get_text()

    doc.close()

    output_path = os.path.join(OUTPUT_DIR, os.path.basename(pdf_path) + ".txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text_output)

    return output_path
