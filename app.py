import streamlit as st
import os, json, re
import pandas as pd
import plotly.express as px

from file_handler import load_uploaded_file
from pdf_time_parser import extract_periods
from financial_signal_extractor import extract_financial_signals
from dashboard_components import metric_card
from llm_client import call_llm

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Virtual CFO | Finance Intelligence",
    layout="wide"
)

# ------------------------------------------------
# HEADER
# ------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
LOGO = os.path.join(BASE_DIR, "compunnel_logo.jpg")

col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists(LOGO):
        st.image(LOGO, width=120)

with col2:
    st.markdown(
        """
        <h2 style="margin-bottom:0;">Virtual CFO – Finance Intelligence</h2>
        <p style="color:gray;">
        Upload → Analyse → Visualize → Ask
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------
for key in [
    "file_loaded",
    "analysis_done",
    "finance_context",
    "metrics",
    "periods",
    "chat_history"
]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# ------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Financial Data (CSV or PDF)",
    type=["csv", "pdf"]
)

# ------------------------------------------------
# ANALYSE BUTTON (MASTER CONTROL)
# ------------------------------------------------
analyse_clicked = st.button("▶ Analyse", type="primary")

if analyse_clicked:
    if not uploaded_file:
        st.warning("Please upload a financial file before clicking Analyse.")
    else:
        with st.spinner("Analysing financial data..."):
            file_type, content = load_uploaded_file(uploaded_file)

            # Store context
            if isinstance(content, pd.DataFrame):
                st.session_state.finance_context = content.to_string()
            else:
                st.session_state.finance_context = content

            # Extract periods
            st.session_state.periods = extract_periods(
                st.session_state.finance_context
            )

            # Extract metrics
            raw_metrics = extract_financial_signals(
                st.session_state.finance_context
            )

            # Safe JSON parsing
            try:
                st.session_state.metrics = json.loads(raw_metrics)
            except Exception:
                match = re.search(r"\{.*\}", raw_metrics, re.S)
                st.session_state.metrics = (
                    json.loads(match.group()) if match else {}
                )

            st.session_state.analysis_done = True
            st.success("Analysis completed successfully")

# ------------------------------------------------
# PANELS (ONLY AFTER ANALYSIS)
# ------------------------------------------------
if st.session_state.analysis_done:

    dashboard_tab, analysis_tab, chat_tab = st.tabs(
        ["📊 Dashboard", "📈 Analysis & Prediction", "🧠 AI CFO Chat"]
    )

    # ==================================================
    # DASHBOARD PANEL
    # ==================================================
    with dashboard_tab:
        st.subheader("📊 Financial Dashboard")

        if st.session_state.periods:
            st.caption(
                f"📅 Detected periods: {', '.join(st.session_state.periods)}"
            )

        metrics = st.session_state.metrics or {}

        c1, c2, c3, c4 = st.columns(4)
        metric_card("Revenue", metrics.get("Revenue"))
        metric_card("EBITDA", metrics.get("EBITDA"))
        metric_card("Net Profit", metrics.get("Net Profit"))
        metric_card(
            "Cash Balance",
            metrics.get("Cash & Cash Equivalents")
        )

        numeric_metrics = {
            k: v for k, v in metrics.items()
            if isinstance(v, (int, float))
        }

        if numeric_metrics:
            df_plot = pd.DataFrame(
                numeric_metrics.items(),
                columns=["Metric", "Value"]
            )

            fig = px.bar(
                df_plot,
                x="Metric",
                y="Value",
                title="Key Financial Metrics Overview",
                text_auto=True
            )

            st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # ANALYSIS / PREDICTION PANEL
    # ==================================================
    with analysis_tab:
        st.subheader("📈 Financial Analysis & Risk Assessment")

        analysis_text = call_llm(
            "You are a senior financial analyst and CFO.",
            f"""
            Using the following financial data, provide:
            - Income Statement analysis
            - Balance Sheet strength
            - Cash Flow health
            - Key financial risks
            - Forward-looking observations

            DATA:
            {st.session_state.finance_context[:5000]}
            """
        )

        st.write(analysis_text)

    # ==================================================
    # AI CFO CHAT PANEL
    # ==================================================
    with chat_tab:
        st.subheader("🧠 AI CFO Assistant")

        user_q = st.chat_input(
            "Ask questions based on the analysed financial data"
        )

        if user_q:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_q}
            )

            answer = call_llm(
                "You are a Virtual CFO answering questions ONLY using the analysed financial data.",
                f"""
                FINANCIAL DATA:
                {st.session_state.finance_context[:5000]}

                QUESTION:
                {user_q}
                """
            )

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
