import pandas as pd
from pdf_loader import extract_pdf_text
from image_ocr import extract_image_text

def route_uploaded_file(uploaded_file):
    """
    Returns:
    - structured_data (DataFrame or None)
    - unstructured_text (str or None)
    """

    name = uploaded_file.name.lower()

    # ---------- CSV / EXCEL ----------
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file), None

    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(uploaded_file), None

    # ---------- PDF ----------
    if name.endswith(".pdf"):
        text = extract_pdf_text(uploaded_file)
        return None, text

    # ---------- IMAGE ----------
    if name.endswith((".png", ".jpg", ".jpeg")):
        text = extract_image_text(uploaded_file)
        return None, text

    return None, None
