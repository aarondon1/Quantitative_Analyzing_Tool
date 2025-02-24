# models/dcf_model.py
import pandas as pd
import numpy as np

def run_dcf(cash_flows, discount_rate):
    """
    Basic DCF model:
    - cash_flows: list of annual CFs
    - discount_rate: decimal (e.g., 0.10 for 10%)
    Returns DataFrame, NPV
    """
    data = []
    for i, cf in enumerate(cash_flows, start=1):
        discount_factor = 1 / ((1 + discount_rate) ** i)
        discounted_cf = cf * discount_factor
        data.append({
            "Year": i,
            "Cash Flow": cf,
            "Discount Factor": round(discount_factor, 4),
            "Discounted CF": round(discounted_cf, 2)
        })
    df = pd.DataFrame(data)
    npv = round(df["Discounted CF"].sum(), 2)
    return df, npv
