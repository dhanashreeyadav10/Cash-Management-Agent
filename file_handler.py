# import pandas as pd
# from pdf_loader import extract_pdf_text

# def load_uploaded_file(uploaded_file):
#     name = uploaded_file.name.lower()

#     if name.endswith(".csv"):
#         return "table", pd.read_csv(uploaded_file)

#     if name.endswith(".pdf"):
#         return "text", extract_pdf_text(uploaded_file)

#     raise ValueError("Unsupported file format")


import pandas as pd
from pdf_loader import extract_pdf_text

def load_uploaded_file(file):
    name = file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(file)
        return "table", df

    if name.endswith(".pdf"):
        return "text", extract_pdf_text(file)

    raise ValueError("Unsupported format")



