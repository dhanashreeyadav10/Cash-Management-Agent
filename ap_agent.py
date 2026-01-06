
import pandas as pd
from llm_client import call_llm

def ap_agent(ap_df):
    ap_df["due_date"] = pd.to_datetime(ap_df["due_date"], errors="coerce")

    late = ap_df[
        (ap_df["payment_status"] == "Unpaid") &
        (ap_df["due_date"] < pd.Timestamp.today())
    ]

    context = f"""
Late unpaid invoices by vendor:
{late.groupby("vendor")["amount"].sum()}
"""

    return call_llm(
        "You are an AP optimization expert.",
        context
    )

