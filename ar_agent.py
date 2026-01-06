# from forecasting import forecast_series
# from llm_client import call_llm

# def ar_agent(ar_df):
#     ar_df["DSO"] = ar_df["days_overdue"] + 30
#     forecast = forecast_series(ar_df["DSO"])

#     context = f"""
# Average DSO: {ar_df["DSO"].mean()}
# Forecasted DSO (next 10 days): {forecast[:10]}
# """

#     return call_llm(
#         "You are an Accounts Receivable strategist.",
#         context + "\nSuggest actions to reduce DSO."
#     )


# from forecasting import forecast_series
# from llm_client import call_llm

# def ar_agent(ar_df=None, text_context=None):
#     if ar_df is not None:
#         ar_df["DSO"] = ar_df["days_overdue"] + 30
#         forecast = forecast_series(ar_df["DSO"])
#         context = f"""
# Average DSO: {ar_df["DSO"].mean()}
# Forecasted DSO: {forecast[:10]}
# """
#     else:
#         context = f"AR Document Text:\n{text_context[:3000]}"

#     return call_llm(
#         "You are an Accounts Receivable strategist.",
#         context + "\nSuggest actions to reduce DSO."
#     )


from forecasting import forecast_series
from llm_client import call_llm

def ar_agent(ar_df):
    ar_df["DSO"] = ar_df["days_overdue"] + 30
    forecast = forecast_series(ar_df["DSO"])

    return call_llm(
        "You are an AR expert.",
        f"Avg DSO: {ar_df['DSO'].mean()}, Forecast: {forecast[:5]}"
    )
