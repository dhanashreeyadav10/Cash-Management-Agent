import re

def extract_periods(text):
    patterns = [
        r"Q[1-4]\s*FY\s*\d{2,4}",
        r"FY\s*\d{2,4}",
        r"Quarter\s+ended\s+[A-Za-z]+\s+\d{1,2},\s*\d{4}",
        r"Year\s+ended\s+[A-Za-z]+\s+\d{1,2},\s*\d{4}"
    ]

    found = set()
    for p in patterns:
        for m in re.findall(p, text, re.IGNORECASE):
            found.add(m.strip())

    return sorted(found)
