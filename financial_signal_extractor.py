from llm_client import call_llm

def extract_financial_signals(text):
    prompt = f"""
Return ONLY valid JSON. No explanations.

Schema:
{{
  "Revenue": number | null,
  "EBITDA": number | null,
  "Net Profit": number | null,
  "Total Assets": number | null,
  "Total Liabilities": number | null,
  "Cash & Cash Equivalents": number | null,
  "Operating Cash Flow": number | null
}}

Document:
{text[:6000]}
"""
    return call_llm("You extract structured financial data.", prompt)
