from forecasting import forecast_series
from llm_client import call_llm

def cash_agent(cash_df):
    cash_df["net_cash"] = cash_df["cash_inflow"] - cash_df["cash_outflow"]
    forecast = forecast_series(cash_df["net_cash"])[:5]

    negative_days = (cash_df["net_cash"] < 0).sum()

    return call_llm(
        "You are a cash flow forecasting expert.",
        f"Negative cash flow days: {negative_days}, Forecast: {forecast}"
    )
