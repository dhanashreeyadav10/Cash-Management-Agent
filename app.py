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
        Investor-grade insights • Risk intelligence • AI-driven explanations
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

data = None
text_context = ""

if uploaded_file:
    file_type, content = load_uploaded_file(uploaded_file)
    if file_type == "table":
        data = content
        st.success("Financial data loaded")
        st.dataframe(data.head())
    else:
        text_context = content
        st.success("Document loaded")

# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Dashboard", "📈 Period Comparison", "🧠 AI CFO Chat", "📄 Reports"]
)

# =================================================
# TAB 1: DASHBOARD
# =================================================
with tab1:
    if data is None:
        st.info("Upload a financial CSV to view dashboard.")
    else:
        st.subheader("📌 Key Financial KPIs")

        def kpi_card(title, value, delta=None):
            st.metric(title, value, delta)

        c1, c2, c3, c4 = st.columns(4)

        revenue = data["revenue"].sum() if "revenue" in data else None
        expenses = data["expenses"].sum() if "expenses" in data else None
        operating_income = revenue - expenses if revenue and expenses else None

        with c1:
            if revenue:
                kpi_card("Revenue", f"₹ {revenue:,.0f}")
        with c2:
            if operating_income:
                kpi_card("Operating Income", f"₹ {operating_income:,.0f}")
        with c3:
            if "debt" in data and "equity" in data:
                de_ratio = data["debt"].sum() / data["equity"].sum()
                kpi_card("Debt / Equity", f"{de_ratio:.2f}")
        with c4:
            if "cash_inflow" in data and "cash_outflow" in data:
                net_cash = (data["cash_inflow"] - data["cash_outflow"]).sum()
                kpi_card("Net Cash Flow", f"₹ {net_cash:,.0f}")

        st.divider()
        st.subheader("📉 Trends")

        if "period" in data and "revenue" in data:
            fig = px.line(
                data,
                x="period",
                y="revenue",
                title="Revenue Trend",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

# =================================================
# TAB 2: PERIOD COMPARISON
# =================================================
with tab2:
    if data is None or "period" not in data:
        st.info("Period comparison requires period-based data.")
    else:
        st.subheader("🆚 Compare Periods")

        periods = data["period"].unique().tolist()
        p1, p2 = st.columns(2)

        with p1:
            old_period = st.selectbox("Select Base Period", periods)
        with p2:
            new_period = st.selectbox("Select Comparison Period", periods, index=len(periods)-1)

        old = data[data["period"] == old_period]
        new = data[data["period"] == new_period]

        if "operating_income" in data:
            old_val = old["operating_income"].sum()
            new_val = new["operating_income"].sum()
            change = new_val - old_val
            pct = (change / old_val) * 100 if old_val else 0

            st.metric(
                "Operating Income Change",
                f"₹ {change:,.0f}",
                f"{pct:.1f}%"
            )

            explanation = call_llm(
                "You are a CFO explaining financial performance.",
                f"""
                Operating income changed from ₹{old_val} to ₹{new_val}.
                Explain drivers and risks in simple investor language.
                """
            )

            st.info(explanation)

# =================================================
# TAB 3: AI CFO CHAT (WITH MEMORY)
# =================================================
with tab3:
    st.subheader("🧠 AI CFO Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_q = st.chat_input("Ask anything about financial performance, risk, cash flow...")

    if user_q:
        st.session_state.chat_history.append({"role": "user", "content": user_q})

        response = call_llm(
            "You are a seasoned CFO answering investor and management questions.",
            f"Context:\n{text_context}\n\nQuestion:\n{user_q}"
        )

        st.session_state.chat_history.append({"role": "assistant", "content": response})

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# =================================================
# TAB 4: REPORTS
# =================================================
with tab4:
    st.subheader("📄 Download Board-Ready Reports")

    if st.button("Generate Reports"):
        insights = {
            "Summary": "Automatically generated CFO insights",
            "Risk": "Liquidity and leverage within acceptable range"
        }

        pdf_path = generate_pdf_report(insights)
        excel_path = generate_excel_report(insights)

        st.download_button("⬇ Download PDF Report", open(pdf_path, "rb"))
        st.download_button("⬇ Download Excel Report", open(excel_path, "rb"))
