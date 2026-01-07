import streamlit as st

def metric_card(title, value, status="neutral", icon=""):
    display = "N/A" if value is None else f"₹ {value:,.0f}"

    colors = {
        "green": "#2ecc71",
        "amber": "#f1c40f",
        "red": "#e74c3c",
        "neutral": "#bdc3c7"
    }

    st.markdown(
        f"""
        <div style="
            border-left:6px solid {colors.get(status)};
            padding:14px;
            border-radius:10px;
            background:#ffffff;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
        ">
            <div style="font-size:14px; color:#555;">
                {icon} {title}
            </div>
            <div style="font-size:22px; font-weight:600;">
                {display}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
