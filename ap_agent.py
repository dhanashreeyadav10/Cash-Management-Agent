import pandas as pd
from llm_client import call_llm

def ap_agent(ap_df):
    ap_df["due_date"] = pd.to_datetime(ap_df["due_date"], errors="coerce")

    late = ap_df[
        (ap_df["payment_status"] == "Unpaid") &
        (ap_df["due_date"] < pd.Timestamp.today())
    ]

    summary = late.groupby("vendor")["amount"].sum().to_string()

    return call_llm(
        "You are an Accounts Payable optimization expert.",
        f"Late unpaid invoices by vendor:\n{summary}"
    )
