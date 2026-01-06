from llm_client import call_llm

def extract_financial_signals(text):
    """
    Converts unstructured PDF into structured financial metrics.
    """

    response = call_llm(
        "You are a financial analyst extracting key metrics.",
        f"""
        From the following financial document, extract approximate values for:
        - Revenue
        - EBITDA
        - Net Profit / PAT
        - Total Assets
        - Total Liabilities
        - Cash & Cash Equivalents
        - Operating Cash Flow

        Return output strictly in JSON with numeric values where possible.

        DOCUMENT:
        {text[:6000]}
        """
    )

    return response
