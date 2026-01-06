def detect_risks(kpis):
    risks = []

    if kpis["Current Ratio"]["value"] < 1:
        risks.append("Liquidity risk: Current Ratio below 1")

    if kpis["Debt/Equity"]["value"] > 1.5:
        risks.append("High leverage risk detected")

    if kpis["Operating Margin"]["value"] < 15:
        risks.append("Margin compression risk")

    return risks
