import pandas as pd
from pdf_loader import extract_pdf_text

def load_uploaded_file(file):
    name = file.name.lower()

    if name.endswith(".csv"):
        return "table", pd.read_csv(file)

    if name.endswith(".pdf"):
        return "text", extract_pdf_text(file)

    raise ValueError("Unsupported file format")
