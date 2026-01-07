import streamlit as st
import os, json, re
import pandas as pd
import plotly.express as px

from file_handler import load_uploaded_file
from pdf_time_parser import extract_periods
from financial_signal_extractor import extract_financial_signals
from dashboard_components import metric_card
from llm_client import call_llm

# ---------------- PAGE ----------------
st.set_page_config("Virtual CFO", layout="wide")

BASE = os.path.dirname(__file__)
st.image(os.path.join(BASE, "compunnel_logo.jpg"), width=120)
st.title("📊 Financial Dashboard – Virtual CFO")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Financial Data (CSV or PDF)", ["csv", "pdf"])

if "context" not in st.session_state:
    st.session_state.context = ""

if uploaded_file:
    file_type, content = load_uploaded_file(uploaded_file)
    st.session_state.context = content if isinstance(content, str) else content.to_string()
    st.success("Document loaded")

# ---------------- DASHBOARD ----------------
st.header("📈 Financial Dashboard")

if st.session_state.context:
    periods = extract_periods(st.session_state.context)
    if periods:
        st.caption(f"📅 Detected periods: {', '.join(periods)}")

    raw = extract_financial_signals(st.session_state.context)

    def safe_json(text):
        try:
            return json.loads(text)
        except:
            match = re.search(r"\{.*\}", text, re.S)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    return {}
        return {}

    metrics = safe_json(raw)

    c1, c2, c3, c4 = st.columns(4)
    metric_card("Revenue", metrics.get("Revenue"))
    metric_card("EBITDA", metrics.get("EBITDA"))
    metric_card("Net Profit", metrics.get("Net Profit"))
    metric_card("Cash Balance", metrics.get("Cash & Cash Equivalents"))

    numeric = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
    if numeric:
        df_plot = pd.DataFrame(numeric.items(), columns=["Metric", "Value"])
        fig = px.bar(df_plot, x="Metric", y="Value", title="Key Financial Metrics")
        st.plotly_chart(fig, use_container_width=True)

# ---------------- AI CFO CHAT ----------------
st.header("🧠 AI CFO Chat")

if "chat" not in st.session_state:
    st.session_state.chat = []

q = st.chat_input("Ask questions about this financial document")

if q:
    st.session_state.chat.append(("user", q))
    a = call_llm(
        "You are a CFO. Answer ONLY using the uploaded financial data.",
        f"{st.session_state.context[:5000]}\n\nQuestion: {q}"
    )
    st.session_state.chat.append(("assistant", a))

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.write(msg)
