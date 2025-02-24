import os
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Load environment variables (Alpha Vantage API key)
from dotenv import load_dotenv
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

def fetch_alpha_vantage(symbol: str, interval="daily", outputsize="compact"):
    """
    Fetch historical stock data from Alpha Vantage.
    interval can be: 'daily', 'weekly', 'monthly' or intraday intervals
    outputsize can be 'compact' (100 data points) or 'full'.
    """
    base_url = "https://www.alphavantage.co/query?"
    if interval == "daily":
        function = "TIME_SERIES_DAILY_ADJUSTED"
    elif interval == "weekly":
        function = "TIME_SERIES_WEEKLY_ADJUSTED"
    elif interval == "monthly":
        function = "TIME_SERIES_MONTHLY_ADJUSTED"
    else:
        # handle intraday
        function = "TIME_SERIES_INTRADAY"
    
    params = {
        "function": function,
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    # For intraday, add interval param
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = interval  # e.g. "15min"

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # The exact keys differ for each function.
        # For daily, "Time Series (Daily)"
        # We'll parse daily as an example:
        if function == "TIME_SERIES_DAILY_ADJUSTED":
            ts_data = data.get("Time Series (Daily)", {})
            records = []
            for date_str, prices in ts_data.items():
                records.append({
                    "Date": date_str,
                    "Open": float(prices["1. open"]),
                    "High": float(prices["2. high"]),
                    "Low": float(prices["3. low"]),
                    "Close": float(prices["4. close"]),
                    "Adj Close": float(prices["5. adjusted close"]),
                    "Volume": float(prices["6. volume"])
                })
            df = pd.DataFrame(records)
            df["Date"] = pd.to_datetime(df["Date"])
            df.sort_values("Date", inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df
        else:
            # Expand for other intervals or intraday as needed
            return pd.DataFrame()
    except Exception as e:
        print("Alpha Vantage API error:", e)
        return pd.DataFrame()

def fetch_yahoo_finance(symbol: str, period="1y", interval="1d"):
    """
    Fetch historical data from Yahoo Finance using yfinance.
    period examples: '1mo', '3mo', '6mo', '1y', '5y', 'max'
    interval examples: '1d', '1wk', '1mo', '1h' etc.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        print("Yahoo Finance API error:", e)
        return pd.DataFrame()
