# risk/risk_manager.py
import numpy as np

def run_risk_analysis(base_value=100, volatility=0.1, simulations=1000):
    """
    Example risk analysis:
    - base_value: starting point
    - volatility: standard deviation for random returns
    - simulations: number of random draws
    Returns a summary text about best/worst-case with probability.
    """
    # Simple random draws from a normal distribution
    returns = np.random.normal(0, volatility, simulations)
    
    # Potential outcomes
    outcomes = base_value * (1 + returns)
    worst_case = np.percentile(outcomes, 5)   # 5th percentile
    best_case  = np.percentile(outcomes, 95)  # 95th percentile
    mean_case  = outcomes.mean()
    
    summary = (
        f"Risk Analysis:\n"
        f" - Mean Outcome: {mean_case:.2f}\n"
        f" - 5% Worst-Case: {worst_case:.2f}\n"
        f" - 95% Best-Case: {best_case:.2f}\n"
        f"Based on {simulations} simulations with volatility={volatility}."
    )
    return summary
