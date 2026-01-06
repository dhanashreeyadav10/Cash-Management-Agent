from llm_client import call_llm

from llm_client import call_llm

def extract_financial_signals(text):
    prompt = f"""
You are a financial data extraction engine.

STRICT RULES:
- Return ONLY valid JSON
- NO comments
- NO calculations
- NO text outside JSON
- All values must be numbers (int or float)
- If a value is not found, return null

JSON SCHEMA (exact keys only):
{{
  "Revenue": number | null,
  "EBITDA": number | null,
  "Net Profit": number | null,
  "Total Assets": number | null,
  "Total Liabilities": number | null,
  "Cash & Cash Equivalents": number | null,
  "Operating Cash Flow": number | null,
  "Gross Margin": number | null,
  "Operating Expenses": number | null,
  "R&D Expense": number | null
}}

DOCUMENT:
{text[:6000]}
"""

    return call_llm(
        "You extract structured financial data.",
        prompt
    )
