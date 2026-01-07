import streamlit as st
import os, json, re
import pandas as pd
import plotly.express as px

from file_handler import load_uploaded_file
from pdf_time_parser import extract_periods
from financial_signal_extractor import extract_financial_signals
from ui_components import metric_card
from llm_client import call_llm

# ---------------- PAGE ----------------
st.set_page_config("Virtual CFO", layout="wide")

BASE = os.path.dirname(__file__)
st.image(os.path.join(BASE, "compunnel_logo.jpg"), width=120)
st.title("📊 Virtual CFO – Financial Intelligence")

# ---------------- STATE INIT ----------------
DEFAULT_METRICS = {
    "Revenue": None,
    "EBITDA": None,
    "Net Profit": None,
    "Total Assets": None,
    "Total Liabilities": None,
    "Cash & Cash Equivalents": None,
    "Operating Cash Flow": None
}

for key, default in {
    "analysis_done": False,
    "finance_context": "",
    "metrics": DEFAULT_METRICS.copy(),
    "periods": [],
    "chat_history": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Financial CSV or PDF", ["csv", "pdf"])

# ---------------- ANALYSE BUTTON ----------------
if st.button("▶ Analyse", type="primary"):
    if not uploaded_file:
        st.warning("Please upload a file first.")
    else:
        with st.spinner("Analysing financial data..."):
            file_type, content = load_uploaded_file(uploaded_file)

            st.session_state.finance_context = (
                content.to_string() if isinstance(content, pd.DataFrame) else content
            )

            st.session_state.periods = extract_periods(
                st.session_state.finance_context
            )

            raw = extract_financial_signals(
                st.session_state.finance_context
            )

            def safe_parse(raw_text):
                try:
                    parsed = json.loads(raw_text)
                    return parsed if isinstance(parsed, dict) else {}
                except Exception:
                    match = re.search(r"\{.*\}", raw_text, re.S)
                    if match:
                        try:
                            return json.loads(match.group())
                        except Exception:
                            pass
                return {}

            parsed = safe_parse(raw)

            final = DEFAULT_METRICS.copy()
            final.update(parsed)

            st.session_state.metrics = final
            st.session_state.analysis_done = True

        st.success("Analysis completed")

# ---------------- PANELS ----------------
if st.session_state.analysis_done:

    dashboard, analysis, chat = st.tabs(
        ["📊 Dashboard", "📈 Analysis & Prediction", "🧠 AI CFO Chat"]
    )

    # ===== DASHBOARD =====
    with dashboard:
        st.subheader("Executive Dashboard")

        if st.session_state.periods:
            st.caption(f"📅 Detected periods: {', '.join(st.session_state.periods)}")

        m = st.session_state.metrics

        c1, c2, c3, c4 = st.columns(4)
        metric_card("Revenue", m.get("Revenue"), "green", "📈")
        metric_card("EBITDA", m.get("EBITDA"), "green", "💹")
        metric_card("Net Profit", m.get("Net Profit"), "amber", "🏦")
        metric_card("Cash Balance", m.get("Cash & Cash Equivalents"), "green", "💰")

        numeric = {k: v for k, v in m.items() if isinstance(v, (int, float))}
        if numeric:
            df = pd.DataFrame(numeric.items(), columns=["Metric", "Value"])
            fig = px.bar(df, x="Metric", y="Value", title="Key Financial Metrics")
            st.plotly_chart(fig, use_container_width=True)

    # ===== ANALYSIS =====
    with analysis:
        st.subheader("Financial Analysis & Risks")

        analysis_text = call_llm(
            "You are a CFO providing investor-grade analysis.",
            st.session_state.finance_context[:5000]
        )
        st.write(analysis_text)

    # ===== CHAT =====
    with chat:
        st.subheader("AI CFO Assistant")

        q = st.chat_input("Ask questions about the analysed financial data")

        if q:
            st.session_state.chat_history.append(("user", q))
            a = call_llm(
                "You are a CFO answering ONLY using the analysed data.",
                f"{st.session_state.finance_context[:5000]}\n\nQuestion: {q}"
            )
            st.session_state.chat_history.append(("assistant", a))

        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.write(msg)
