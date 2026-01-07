def compare_periods(old, new, label):
    diff = new - old
    pct = (diff / old) * 100 if old else 0

    direction = "increased" if diff > 0 else "decreased"

    summary = (
        f"{label} {direction} by ₹{abs(diff):,.0f} "
        f"({pct:.1f}%), primarily driven by core business performance."
    )

    return diff, pct, summary
