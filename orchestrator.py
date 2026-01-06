# from ap_agent import ap_agent
# from ar_agent import ar_agent
# from cash_agent import cash_agent

# def run_finance_agents(ap_df, ar_df, cash_df):
#     return {
#         "AP Insights": ap_agent(ap_df),
#         "AR Insights": ar_agent(ar_df),
#         "Cash Insights": cash_agent(cash_df)
#     }


# from ap_agent import ap_agent
# from ar_agent import ar_agent
# from cash_agent import cash_agent

# def run_finance_agents(df=None, text=None):
#     return {
#         "AP Insights": ap_agent(df, text),
#         "AR Insights": ar_agent(df, text),
#         "Cash Insights": cash_agent(df, text),
#     }


# from ap_agent import ap_agent
# from ar_agent import ar_agent
# from cash_agent import cash_agent
# from llm_client import call_llm

# def run_finance_agents(data_type, data):
#     if data_type == "structured":
#         return {
#             "AP Insights": ap_agent(data),
#             "AR Insights": ar_agent(data),
#             "Cash Insights": cash_agent(data),
#         }

#     # Unstructured (PDF / Image / Text)
#     context = f"""
# Financial document content:
# {str(data)[:3000]}
# """

#     return {
#         "Document Insights": call_llm(
#             "You are a senior finance analyst.",
#             context + "\nExtract risks, insights, and recommendations."
#         )
#     }


from ap_agent import ap_agent
from ar_agent import ar_agent
from cash_agent import cash_agent
from llm_client import call_llm

def run_finance_analysis(file_type, content):
    # Case 1: Structured data (CSV / Excel)
    if file_type == "table":
        insights = {}

        if {"vendor","amount","payment_status","due_date"}.issubset(content.columns):
            insights["AP Insights"] = ap_agent(content)

        if {"days_overdue"}.issubset(content.columns):
            insights["AR Insights"] = ar_agent(content)

        if {"cash_inflow","cash_outflow"}.issubset(content.columns):
            insights["Cash Insights"] = cash_agent(content)

        return insights

    # Case 2: Unstructured documents (PDF / Image)
    else:
        return {
            "Document Insights": call_llm(
                "You are a senior finance analyst.",
                f"Analyze this financial document and provide insights:\n{content[:4000]}"
            )
        }
