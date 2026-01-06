# import pdfplumber

# def extract_pdf_text(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             if page.extract_text():
#                 text += page.extract_text() + "\n"
#     return text

import pdfplumber

def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            if p.extract_text():
                text += p.extract_text()
    return text
