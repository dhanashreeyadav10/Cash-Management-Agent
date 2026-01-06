import pandas as pd
import re

def parse_finance_text_to_df(text: str):
    """
    VERY SIMPLE parser for PoC.
    You can improve later using NLP / regex.
    """
    rows = []
    for line in text.split("\n"):
        if re.search(r"\d", line):
            rows.append({"raw_text": line})

    return pd.DataFrame(rows)
