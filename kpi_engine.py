def compute_kpis(metrics):
    """
    metrics: extracted numeric dictionary
    """
    kpis = {}

    # Profitability
    if metrics.get("Revenue") and metrics.get("Net Profit"):
        net_margin = metrics["Net Profit"] / metrics["Revenue"] * 100
        kpis["Net Margin"] = (net_margin, "green" if net_margin > 15 else "amber")

    # Liquidity
    if metrics.get("Total Assets") and metrics.get("Total Liabilities"):
        current_ratio = metrics["Total Assets"] / metrics["Total Liabilities"]
        kpis["Current Ratio"] = (
            current_ratio,
            "green" if current_ratio > 1.5 else "amber" if current_ratio > 1 else "red"
        )

    # Leverage
    if metrics.get("Total Liabilities") and metrics.get("Total Assets"):
        debt_equity = metrics["Total Liabilities"] / metrics["Total Assets"]
        kpis["Debt / Equity"] = (
            debt_equity,
            "green" if debt_equity < 0.8 else "amber"
        )

    return kpis
