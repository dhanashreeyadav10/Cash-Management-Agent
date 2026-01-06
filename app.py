import streamlit as st
import pandas as pd
import traceback
import os

from file_handler import load_uploaded_file
from orchestrator import run_finance_analysis
from excel_report import generate_excel_report
from pdf_report import generate_pdf_report

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="Finance AI Agent",
    layout="wide"
)

# ----------------------------------------------------
# LOGO + HEADER (ROBUST IMPLEMENTATION)
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "compunnel_logo.jpg")

col1, col2 = st.columns([1, 7])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=130)
    else:
        st.error("Logo not found")

with col2:
    st.markdown(
        """
        <h2 style="margin-bottom:0;">Finance AI Agent</h2>
        <p style="color:gray;">
            Accounts Payable • Accounts Receivable • Cash Flow • Forecasting
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ----------------------------------------------------
# FILE UPLOAD
# ----------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Finance File (CSV or PDF)",
    type=["csv", "pdf"]
)

file_type = None
content = None

if uploaded_file:
    try:
        file_type, content = load_uploaded_file(uploaded_file)
        st.success("File loaded successfully")

        if file_type == "table":
            st.subheader("Preview Data")
            st.dataframe(content.head())
        else:
            st.subheader("Extracted Text")
            st.text_area("Document Content", content[:2000], height=250)

    except Exception:
        st.error("File processing failed")
        st.code(traceback.format_exc())

# ----------------------------------------------------
# RUN ANALYSIS
# ----------------------------------------------------
if st.button("🚀 Run Finance Analysis") and uploaded_file:
    try:
        insights = run_finance_analysis(file_type, content)

        if not insights:
            st.warning("No insights could be generated from this file.")
        else:
            for k, v in insights.items():
                st.subheader(k)
                st.write(v)

            # -------------------------------
            # REPORT GENERATION
            # -------------------------------
            excel_path = generate_excel_report(
                content if file_type == "table" else pd.DataFrame(),
                pd.DataFrame(),
                pd.DataFrame(),
                insights
            )

            pdf_path = generate_pdf_report(insights)

            st.divider()
            st.subheader("📥 Download Reports")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                st.download_button(
                    "⬇ Download Excel Report",
                    data=open(excel_path, "rb"),
                    file_name="Finance_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            with col_dl2:
                st.download_button(
                    "⬇ Download PDF Report",
                    data=open(pdf_path, "rb"),
                    file_name="Finance_Report.pdf",
                    mime="application/pdf"
                )

    except Exception:
        st.error("Finance analysis failed")
        st.code(traceback.format_exc())
