import streamlit as st
import pandas as pd
import traceback

from file_handler import load_uploaded_file
from orchestrator import run_finance_analysis
from excel_report import generate_excel_report
from pdf_report import generate_pdf_report

st.set_page_config(page_title="Finance AI Agent", layout="wide")
st.title("💰 Finance AI Agent")

uploaded_file = st.file_uploader(
    "Upload PDF / Image / CSV",
    type=["pdf", "csv", "png", "jpg", "jpeg"]
)

file_type = None
content = None

if uploaded_file:
    try:
        file_type, content = load_uploaded_file(uploaded_file)
        st.success("File loaded successfully")

        if file_type == "table":
            st.dataframe(content.head())
        else:
            st.text_area("Extracted Text", content[:2000])

    except Exception:
        st.error("File processing failed")
        st.code(traceback.format_exc())

if st.button("🚀 Run Finance Analysis") and uploaded_file:
    insights = run_finance_analysis(file_type, content)

    for k, v in insights.items():
        st.subheader(k)
        st.write(v)

    # Reports
    excel_path = generate_excel_report(
        content if file_type=="table" else pd.DataFrame(),
        pd.DataFrame(),
        pd.DataFrame(),
        insights
    )

    pdf_path = generate_pdf_report(insights)

    st.download_button("⬇ Download Excel Report", open(excel_path,"rb"), "Finance_Report.xlsx")
    st.download_button("⬇ Download PDF Report", open(pdf_path,"rb"), "Finance_Report.pdf")
