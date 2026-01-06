import pandas as pd

def generate_excel_report(ap_df, ar_df, cash_df, insights):
    path = "finance_analysis_report.xlsx"

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        ap_df.to_excel(writer, sheet_name="AP", index=False)
        ar_df.to_excel(writer, sheet_name="AR", index=False)
        cash_df.to_excel(writer, sheet_name="Cash", index=False)

        pd.DataFrame({
            "Area": insights.keys(),
            "Insights": insights.values()
        }).to_excel(writer, sheet_name="AI Insights", index=False)

    return path
