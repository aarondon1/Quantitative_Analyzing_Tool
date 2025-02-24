# models/consolidation_model.py
import pandas as pd

def run_consolidation(subsidiary_data):
    """
    Example Consolidation Model:
    - subsidiary_data: list of dicts with ["Name", "Revenue", "Expenses"], etc.
    Returns DataFrame of consolidated data + summary
    """
    df = pd.DataFrame(subsidiary_data)
    df["NetIncome"] = df["Revenue"] - df["Expenses"]
    total_revenue = df["Revenue"].sum()
    total_expenses = df["Expenses"].sum()
    total_net_income = df["NetIncome"].sum()
    summary = (
        f"Consolidated Revenue: {total_revenue}, "
        f"Expenses: {total_expenses}, "
        f"Net Income: {total_net_income}"
    )
    return df, summary
