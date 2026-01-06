# import streamlit as st
# import pandas as pd
# import traceback
# import os

# from file_handler import load_uploaded_file
# from orchestrator import run_finance_analysis
# from excel_report import generate_excel_report
# from pdf_report import generate_pdf_report

# # ----------------------------------------------------
# # PAGE CONFIG
# # ----------------------------------------------------
# st.set_page_config(
#     page_title="Finance AI Agent",
#     layout="wide"
# )

# # ----------------------------------------------------
# # LOGO + HEADER (ROBUST IMPLEMENTATION)
# # ----------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOGO_PATH = os.path.join(BASE_DIR, "compunnel_logo.jpg")

# col1, col2 = st.columns([1, 7])

# with col1:
#     if os.path.exists(LOGO_PATH):
#         st.image(LOGO_PATH, width=130)
#     else:
#         st.error("Logo not found")

# with col2:
#     st.markdown(
#         """
#         <h2 style="margin-bottom:0;">Finance AI Agent</h2>
#         <p style="color:gray;">
#             Accounts Payable • Accounts Receivable • Cash Flow • Forecasting
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

# st.divider()

# # ----------------------------------------------------
# # FILE UPLOAD
# # ----------------------------------------------------
# uploaded_file = st.file_uploader(
#     "Upload Finance File (CSV or PDF)",
#     type=["csv", "pdf"]
# )

# file_type = None
# content = None

# if uploaded_file:
#     try:
#         file_type, content = load_uploaded_file(uploaded_file)
#         st.success("File loaded successfully")

#         if file_type == "table":
#             st.subheader("Preview Data")
#             st.dataframe(content.head())
#         else:
#             st.subheader("Extracted Text")
#             st.text_area("Document Content", content[:2000], height=250)

#     except Exception:
#         st.error("File processing failed")
#         st.code(traceback.format_exc())

# # ----------------------------------------------------
# # RUN ANALYSIS
# # ----------------------------------------------------
# if st.button("🚀 Run Finance Analysis") and uploaded_file:
#     try:
#         insights = run_finance_analysis(file_type, content)

#         if not insights:
#             st.warning("No insights could be generated from this file.")
#         else:
#             for k, v in insights.items():
#                 st.subheader(k)
#                 st.write(v)

#             # -------------------------------
#             # REPORT GENERATION
#             # -------------------------------
#             excel_path = generate_excel_report(
#                 content if file_type == "table" else pd.DataFrame(),
#                 pd.DataFrame(),
#                 pd.DataFrame(),
#                 insights
#             )

#             pdf_path = generate_pdf_report(insights)

#             st.divider()
#             st.subheader("📥 Download Reports")

#             col_dl1, col_dl2 = st.columns(2)

#             with col_dl1:
#                 st.download_button(
#                     "⬇ Download Excel Report",
#                     data=open(excel_path, "rb"),
#                     file_name="Finance_Report.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                 )

#             with col_dl2:
#                 st.download_button(
#                     "⬇ Download PDF Report",
#                     data=open(pdf_path, "rb"),
#                     file_name="Finance_Report.pdf",
#                     mime="application/pdf"
#                 )

#     except Exception:
#         st.error("Finance analysis failed")
#         st.code(traceback.format_exc())


import streamlit as st
import pandas as pd
import os
import plotly.express as px

from llm_client import call_llm
from file_handler import load_uploaded_file
from pdf_report import generate_pdf_report
from excel_report import generate_excel_report

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Virtual CFO | Finance Intelligence",
    layout="wide"
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
LOGO = os.path.join(BASE_DIR, "compunnel_logo.jpg")

col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists(LOGO):
        st.image(LOGO, width=120)
with col2:
    st.markdown(
        """
        <h2 style="margin-bottom:0;">Virtual CFO – Finance Intelligence Platform</h2>
        <p style="color:gray;">
        Document-driven insights • Investor-grade analysis • AI CFO Assistant
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Financial Data (CSV or PDF)",
    type=["csv", "pdf"]
)

if "finance_context" not in st.session_state:
    st.session_state.finance_context = ""

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

if uploaded_file:
    file_type, content = load_uploaded_file(uploaded_file)

    if file_type == "table":
        st.session_state.dataframe = content
        st.session_state.finance_context = content.head(200).to_string()
        st.success("Structured financial data loaded")

    else:
        st.session_state.dataframe = None
        st.session_state.finance_context = content
        st.success("Financial document loaded and indexed")

# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "📊 Financial Analysis & Comparison", "🧠 AI CFO Chat", "📄 Reports"]
)

# =================================================
# TAB 1: DASHBOARD (AUTO VISUAL)
# =================================================
with tab1:
    if not st.session_state.finance_context:
        st.info("Upload a financial file to view dashboard insights.")
    else:
        st.subheader("📌 Key Financial Highlights")

        # ---------- AI SUMMARY ----------
        summary = call_llm(
            "You are a CFO summarizing financial performance.",
            f"Provide 5 concise bullet insights from this financial data:\n{st.session_state.finance_context[:4000]}"
        )

        st.success(summary)

        # ---------- CSV VISUALS ----------
        if st.session_state.dataframe is not None:
            df = st.session_state.dataframe

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                col = st.selectbox("Select metric to visualize", numeric_cols)
                fig = px.line(df, y=col, title=f"{col} Trend")
                st.plotly_chart(fig, use_container_width=True)

# =================================================
# TAB 2: FULL FINANCIAL ANALYSIS
# =================================================
with tab2:
    if not st.session_state.finance_context:
        st.info("Upload a financial file to run analysis.")
    else:
        st.subheader("📊 Comprehensive Financial Analysis")

        analysis = call_llm(
            "You are a senior financial analyst and CFO.",
            f"""
            Analyze the following financial data/document and provide:
            - Income Statement insights
            - Balance Sheet strength
            - Cash Flow health
            - Key risks (liquidity, leverage, margin, cash)
            - Period comparison insights if available
            Use professional, investor-ready language.

            DATA:
            {st.session_state.finance_context[:5000]}
            """
        )

        st.write(analysis)

# =================================================
# TAB 3: AI CFO CHAT (FILE-GROUNDED)
# =================================================
with tab3:
    st.subheader("🧠 AI CFO Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_q = st.chat_input("Ask questions based on the uploaded financial data")

    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})

        response = call_llm(
            "You are a Virtual CFO answering questions ONLY based on the provided financial data.",
            f"""
            FINANCIAL DATA:
            {st.session_state.finance_context[:5000]}

            QUESTION:
            {user_q}
            """
        )

        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# =================================================
# TAB 4: REPORTS
# =================================================
with tab4:
    st.subheader("📄 Board-Ready Reports")

    if st.button("Generate Structured Reports"):
        insights = {
            "Financial Analysis": st.session_state.finance_context[:2000]
        }

        pdf_path = generate_pdf_report(insights)
        excel_path = generate_excel_report(insights)

        st.download_button("⬇ Download PDF Report", open(pdf_path, "rb"))
        st.download_button("⬇ Download Excel Report", open(excel_path, "rb"))
