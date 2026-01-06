
import pandas as pd
from pdf_loader import extract_pdf_text
from image_ocr import extract_image_text

def load_uploaded_file(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return "table", df

    elif name.endswith(".pdf"):
        text = extract_pdf_text(uploaded_file)
        return "text", text

    elif name.endswith((".png", ".jpg", ".jpeg")):
        text = extract_image_text(uploaded_file)
        return "text", text

    else:
        raise ValueError("Unsupported file format")

