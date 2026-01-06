import streamlit as st

def metric_card(title, value, status="neutral"):
    color = {
        "good": "#2ecc71",
        "warn": "#f1c40f",
        "bad": "#e74c3c",
        "neutral": "#bdc3c7"
    }[status]

    st.markdown(
        f"""
        <div style="
            border-left:6px solid {color};
            padding:14px;
            border-radius:8px;
            background:#fafafa;
        ">
            <b>{title}</b>
            <h3>{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
