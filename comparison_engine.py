def compare(old, new, metric):
    diff = new - old
    pct = (diff / old) * 100

    return (
        f"{metric} increased by ₹{diff:.1f} Cr "
        f"({pct:.1f}%), driven by operational improvements."
    )
