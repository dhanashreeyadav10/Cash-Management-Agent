# --- inside app.py after Analyse is completed ---

from ui_components import metric_card, sparkline
from kpi_engine import compute_kpis
from comparison_engine import compare_periods

dashboard, income, balance, cashflow, kpi_tab, compare_tab, chat_tab = st.tabs(
    [
        "📊 Executive Dashboard",
        "📈 Income Statement",
        "🧮 Balance Sheet",
        "💰 Cash Flow",
        "📊 KPI & Ratios",
        "🔄 Period Comparison",
        "🧠 AI CFO Assistant"
    ]
)

# ================= EXECUTIVE DASHBOARD =================
with dashboard:
    st.subheader("Executive Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    metric_card("Revenue", "₹119,575 Cr", "↑ YoY", "green", "📈")
    metric_card("EBITDA", "₹40,820 Cr", "↑ Margin Expansion", "green", "💹")
    metric_card("Net Profit", "₹33,916 Cr", "Stable", "amber", "🏦")
    metric_card("Cash Balance", "₹40,760 Cr", "Strong Liquidity", "green", "💰")

# ================= INCOME STATEMENT =================
with income:
    st.subheader("Income Statement Insights")

    c1, c2, c3 = st.columns(3)
    metric_card("Revenue Growth", "↑ 8.4% YoY", status="green", icon="📈")
    metric_card("Margin Trend", "↑ 120 bps", status="green", icon="📊")
    metric_card("Expense Efficiency", "82 / 100", status="amber", icon="⚙️")

    sparkline([100, 108, 115, 119])

# ================= BALANCE SHEET =================
with balance:
    st.subheader("Balance Sheet Strength")

    c1, c2, c3 = st.columns(3)
    metric_card("Current Ratio", "1.4x", status="amber", icon="🧮")
    metric_card("Debt / Equity", "0.79x", status="green", icon="🏦")
    metric_card("Asset Quality", "No Red Flags", status="green", icon="🛡️")

# ================= CASH FLOW =================
with cashflow:
    st.subheader("Cash Flow Health")

    c1, c2, c3 = st.columns(3)
    metric_card("Operating Cash Flow", "Healthy", status="green", icon="💰")
    metric_card("Free Cash Flow", "Positive Trend", status="green", icon="📊")
    metric_card("Cash Burn", "No Concern", status="green", icon="🔥")

# ================= KPI & RATIOS =================
with kpi_tab:
    st.subheader("Investor-Grade KPI Dashboard")

    kpis = compute_kpis(st.session_state.metrics)
    cols = st.columns(3)

    for col, (kpi, (val, status)) in zip(cols * 3, kpis.items()):
        with col:
            metric_card(kpi, f"{val:.2f}", status=status)

# ================= PERIOD COMPARISON =================
with compare_tab:
    st.subheader("Period Comparison Engine")

    diff, pct, summary = compare_periods(
        old=70100,
        new=74248,
        label="Operating Income"
    )

    st.metric("Operating Income Change", f"₹{diff:,.0f}", f"{pct:.1f}%")
    st.info(summary)

# ================= AI CFO CHAT =================
with chat_tab:
    st.subheader("AI CFO Assistant")

    q = st.chat_input("Ask questions like a board member or investor")

    if q:
        st.session_state.chat_history.append(("user", q))
        a = call_llm(
            "You are a Virtual CFO. Answer professionally using the analysed data.",
            q
        )
        st.session_state.chat_history.append(("assistant", a))

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)
