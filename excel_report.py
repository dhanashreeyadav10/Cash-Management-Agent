import pandas as pd

def generate_excel_report(ap_df, ar_df, cash_df, insights):
    path = "finance_report.xlsx"

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        ap_df.to_excel(writer, "AP", index=False)
        ar_df.to_excel(writer, "AR", index=False)
        cash_df.to_excel(writer, "Cash", index=False)

        pd.DataFrame({
            "Section": insights.keys(),
            "Insight": insights.values()
        }).to_excel(writer, "AI Insights", index=False)

    return path
