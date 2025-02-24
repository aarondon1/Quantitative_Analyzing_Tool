# models/forecasting_model.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def run_forecasting(historical_data):
    """
    Placeholder Forecasting model:
    - historical_data: DataFrame with columns ["Date", "Close"] at least
    We'll do a naive forecast: next 12 steps = last close + random noise
    Returns forecast DataFrame and a base64-encoded plot
    """
    if historical_data.empty:
        return pd.DataFrame(), ""

    last_close = historical_data["Close"].iloc[-1]
    future_dates = pd.date_range(
        start=historical_data["Date"].iloc[-1],
        periods=12, freq="M"
    )
    forecast_values = [last_close + np.random.normal(0, 2) for _ in range(12)]
    forecast_df = pd.DataFrame({"Date": future_dates, "Forecast": forecast_values})
    
    # Plot
    fig, ax = plt.subplots()
    ax.plot(historical_data["Date"], historical_data["Close"], label="Historical")
    ax.plot(forecast_df["Date"], forecast_df["Forecast"], label="Forecast", marker='o')
    ax.legend()
    ax.set_title("Naive Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)
    
    return forecast_df, plot_base64
