
import numpy as np
import pandas as pd

def calculate_metrics(returns, risk_free_rate=0.0):
    # Remove missing values
    returns = pd.Series(returns).dropna()

    if returns.empty:
        raise ValueError("No returns provided.")

    trading_days = 252
    n = len(returns)

    # 1. Cumulative Return
    growth = (1 + returns).cumprod()
    cumulative_return = growth.iloc[-1] - 1

    # 2. Annualized Return (CAGR approximation)
    if growth.iloc[-1] > 0:
        annualized_return = (
            growth.iloc[-1] ** (trading_days / n) - 1
        )
    else:
        annualized_return = -1.0

    # 3. Annualized Volatility
    volatility = returns.std() * np.sqrt(trading_days)

    # 4. Sharpe Ratio
    # Annualized Sharpe Ratio
    daily_risk_free_rate = (1 + risk_free_rate) ** (1 / 252) - 1
    excess_returns = returns - daily_risk_free_rate
    if returns.std() > 0:
        sharpe_ratio = (
            excess_returns.mean()
            / returns.std()
            * np.sqrt(252)
        )
    else:
        sharpe_ratio = np.nan

    # 5. Maximum Drawdown
    running_peak = growth.cummax()
    drawdown = growth / running_peak - 1
    max_drawdown = drawdown.min()

    return {
        "Cumulative Return": cumulative_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Maximum Drawdown": max_drawdown
    }
