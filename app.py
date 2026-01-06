
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
from pdf_time_parser import extract_periods
from financial_signal_extractor import extract_financial_signals
from dashboard_components import metric_card
import plotly.express as px
import json

with tab1:
    st.subheader("📊 Financial Dashboard")

    if not st.session_state.finance_context:
        st.info("Upload a financial document to generate insights.")
    else:
        # ---------- PERIOD DETECTION ----------
        periods = extract_periods(st.session_state.finance_context)
        if periods:
            st.caption(f"📅 Detected Periods: {', '.join(periods)}")

        # ---------- EXTRACT SIGNALS ----------
        with st.spinner("Extracting financial signals..."):
            raw_metrics = extract_financial_signals(
                st.session_state.finance_context
            )

        try:
            metrics = json.loads(raw_metrics)
        except Exception:
            st.error("Could not structure financial metrics.")
            st.write(raw_metrics)
            metrics = {}

        # ---------- METRIC CARDS ----------
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("Revenue", metrics.get("Revenue", "N/A"), "good")
        with c2:
            metric_card("EBITDA", metrics.get("EBITDA", "N/A"), "good")
        with c3:
            metric_card("Net Profit", metrics.get("Net Profit", "N/A"))
        with c4:
            metric_card("Cash Balance", metrics.get("Cash & Cash Equivalents", "N/A"))

        st.divider()

        # ---------- GRAPHICAL VIEW ----------
        numeric_metrics = {
            k: v for k, v in metrics.items()
            if isinstance(v, (int, float))
        }

        if numeric_metrics:
            df_plot = (
                pd.DataFrame.from_dict(
                    numeric_metrics, orient="index", columns=["Value"]
                )
                .reset_index()
                .rename(columns={"index": "Metric"})
            )

            fig = px.bar(
                df_plot,
                x="Metric",
                y="Value",
                title="Key Financial Metrics Overview",
                text_auto=True
            )

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

