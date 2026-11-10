
import pandas as pd
from metrics import calculate_metrics

# Load historical data
data = pd.read_csv(
    "aapl_data.csv",
    index_col=0,
    parse_dates=True
)

# Daily market returns
data["Market_Return"] = data["Close"].pct_change().fillna(0)

# Strategy parameters to compare
strategies = [
    (10, 30),
    (20, 50),
    (50, 200)
]

transaction_cost = 0.001
results = []

for short_window, long_window in strategies:

    # Calculate moving averages
    short_sma = data["Close"].rolling(short_window).mean()
    long_sma = data["Close"].rolling(long_window).mean()

    # Generate trading signals
    signal = (short_sma > long_sma).astype(int)

    # Avoid look-ahead bias
    position = signal.shift(1).fillna(0)

    # Count position changes
    trades = position.diff().abs().fillna(0)

    # Calculate strategy returns
    strategy_returns = (
        position * data["Market_Return"]
        - trades * transaction_cost
    )

    # Calculate performance metrics
    metrics = calculate_metrics(strategy_returns)

    metrics["Strategy"] = f"SMA {short_window}/{long_window}"
    metrics["Trades"] = int(trades.sum())

    results.append(metrics)

# Create comparison table
results_df = pd.DataFrame(results).set_index("Strategy")

print("\n--- Strategy Comparison ---")
print(results_df.round(4))

# Save results
results_df.to_csv("strategy_comparison.csv")
