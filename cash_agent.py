# from forecasting import forecast_series
# from llm_client import call_llm

# def cash_agent(cash_df):
#     cash_df["net_cash"] = cash_df["cash_inflow"] - cash_df["cash_outflow"]
#     forecast = forecast_series(cash_df["net_cash"])

#     context = f"""
# Negative cash days: {(cash_df["net_cash"] < 0).sum()}
# Forecasted net cash (next 10 days): {forecast[:10]}
# """

#     return call_llm(
#         "You are a cash flow optimization expert.",
#         context + "\nProvide liquidity recommendations."
#     )


# from forecasting import forecast_series
# from llm_client import call_llm

# def cash_agent(cash_df=None, text_context=None):
#     if cash_df is not None:
#         cash_df["net_cash"] = cash_df["cash_inflow"] - cash_df["cash_outflow"]
#         forecast = forecast_series(cash_df["net_cash"])
#         context = f"""
# Negative cash days: {(cash_df["net_cash"] < 0).sum()}
# Forecasted cash: {forecast[:10]}
# """
#     else:
#         context = f"Cash Document Text:\n{text_context[:3000]}"

#     return call_llm(
#         "You are a cash flow optimization expert.",
#         context + "\nProvide liquidity recommendations."
#     )


from forecasting import forecast_series
from llm_client import call_llm

def cash_agent(cash_df):
    cash_df["net_cash"] = cash_df["cash_inflow"] - cash_df["cash_outflow"]
    forecast = forecast_series(cash_df["net_cash"])

    return call_llm(
        "You are a cash flow expert.",
        f"Negative days: {(cash_df['net_cash'] < 0).sum()}, Forecast: {forecast[:5]}"
    )
