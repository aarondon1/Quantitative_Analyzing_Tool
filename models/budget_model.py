# models/budget_model.py
import pandas as pd

def run_budget(budget_items):
    """
    Budget Model:
    - budget_items: list of dict with ["Category", "Budgeted", "Actual"]
    Returns DataFrame + summary on variance
    """
    df = pd.DataFrame(budget_items)
    df["Variance"] = df["Budgeted"] - df["Actual"]
    total_variance = df["Variance"].sum()
    summary = f"Total Budget Variance: {total_variance}"
    return df, summary
