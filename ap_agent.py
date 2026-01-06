# import pandas as pd
# from llm_client import call_llm

# def ap_agent(ap_df):
#     ap_df["due_date"] = pd.to_datetime(ap_df["due_date"], errors="coerce")

#     late = ap_df[
#         (ap_df["payment_status"] == "Unpaid") &
#         (ap_df["due_date"] < pd.Timestamp.today())
#     ]

#     context = f"""
# Late unpaid invoices by vendor:
# {late.groupby("vendor")["amount"].sum()}
# """

#     return call_llm(
#         "You are an AP optimization expert.",
#         context + "\nProvide improvement recommendations."
#     )

# import pandas as pd
# from llm_client import call_llm

# def ap_agent(ap_df: pd.DataFrame):

#     # ✅ Ensure due_date is datetime
#     ap_df["due_date"] = pd.to_datetime(ap_df["due_date"], errors="coerce")

#     # Drop rows where date parsing failed
#     ap_df = ap_df.dropna(subset=["due_date"])

#     late = ap_df[
#         (ap_df["payment_status"] == "Unpaid") &
#         (ap_df["due_date"] < pd.Timestamp.today())
#     ]

#     if late.empty:
#         return "No overdue unpaid invoices found."

#     context = f"""
# Overdue unpaid invoices by vendor:
# {late.groupby("vendor")["amount"].sum()}
# """

#     return call_llm(
#         "You are an Accounts Payable optimization expert.",
#         context + "\nProvide clear recommendations to reduce delays and penalties."
#     )


# import pandas as pd
# from llm_client import call_llm

# def ap_agent(ap_df=None, text_context=None):
#     if ap_df is not None:
#         ap_df["due_date"] = pd.to_datetime(ap_df["due_date"], errors="coerce")
#         late = ap_df[
#             (ap_df["payment_status"] == "Unpaid") &
#             (ap_df["due_date"] < pd.Timestamp.today())
#         ]
#         context = f"AP Table Analysis:\n{late.groupby('vendor')['amount'].sum()}"
#     else:
#         context = f"AP Document Text:\n{text_context[:3000]}"

#     return call_llm(
#         "You are an Accounts Payable optimization expert.",
#         context + "\nGive actionable AP recommendations."
#     )

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
