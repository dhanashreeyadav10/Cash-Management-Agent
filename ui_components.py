import streamlit as st
import plotly.graph_objects as go

def metric_card(title, value, delta=None, status="neutral", icon=""):
    color_map = {
        "green": "#2ecc71",
        "amber": "#f1c40f",
        "red": "#e74c3c",
        "neutral": "#bdc3c7"
    }

    st.markdown(
        f"""
        <div style="
            border-left:6px solid {color_map[status]};
            padding:14px;
            border-radius:10px;
            background:#ffffff;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
        ">
            <div style="font-size:14px; color:#555;">
                {icon} {title}
            </div>
            <div style="font-size:22px; font-weight:600;">
                {value}
            </div>
            <div style="font-size:12px; color:#777;">
                {delta if delta else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def sparkline(data):
    fig = go.Figure(
        go.Scatter(
            y=data,
            mode="lines",
            line=dict(width=2),
        )
    )
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    st.plotly_chart(fig, use_container_width=True)
