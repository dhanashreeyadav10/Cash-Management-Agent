
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

