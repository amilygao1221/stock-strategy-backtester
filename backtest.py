
import pandas as pd
import matplotlib.pyplot as plt
from metrics import calculate_metrics

# 1. Load data
data = pd.read_csv(
    "aapl_data.csv",
    index_col=0,
    parse_dates=True
)

# 2. Calculate moving averages
data["SMA_20"] = data["Close"].rolling(20).mean()
data["SMA_50"] = data["Close"].rolling(50).mean()

# 3. Generate trading signals
data["Signal"] = (
    data["SMA_20"] > data["SMA_50"]
).astype(int)

# 4. Avoid look-ahead bias
data["Position"] = data["Signal"].shift(1).fillna(0)

# 5. Calculate daily stock returns
data["Market_Return"] = data["Close"].pct_change().fillna(0)

# 6. Calculate strategy returns
data["Strategy_Return"] = (
    data["Position"] * data["Market_Return"]
)

# 7. Apply transaction costs
transaction_cost = 0.001  # 0.1% per position change

data["Trades"] = (
    data["Position"].diff().abs().fillna(0)
)

data["Strategy_Return"] = (
    data["Strategy_Return"]
    - data["Trades"] * transaction_cost
)

# 8. Calculate portfolio values
initial_capital = 10000

data["Buy_Hold_Value"] = (
    initial_capital
    * (1 + data["Market_Return"]).cumprod()
)

data["Strategy_Value"] = (
    initial_capital
    * (1 + data["Strategy_Return"]).cumprod()
)

# 9. Print results
print("\n--- Backtest Results ---")

print(
    "Buy & Hold Final Value: $",
    round(data["Buy_Hold_Value"].iloc[-1], 2)
)

print(
    "SMA Strategy Final Value: $",
    round(data["Strategy_Value"].iloc[-1], 2)
)

print(
    "Total Position Changes:",
    int(data["Trades"].sum())
)

# 10. Plot portfolio performance
plt.figure(figsize=(11, 6))

plt.plot(
    data.index,
    data["Buy_Hold_Value"],
    label="Buy & Hold"
)

plt.plot(
    data.index,
    data["Strategy_Value"],
    label="SMA 20/50 Strategy"
)

plt.title("AAPL Backtest: Buy & Hold vs SMA Crossover")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("backtest_comparison.png", dpi=200)
plt.show()


# 11. Calculate performance metrics
buy_hold_metrics = calculate_metrics(data["Market_Return"])
sma_metrics = calculate_metrics(data["Strategy_Return"])

print("\n--- Performance Metrics ---")

results = pd.DataFrame({
    "Buy & Hold": buy_hold_metrics,
    "SMA 20/50": sma_metrics
})

print(results.round(4))

# Save metrics for future analysis
results.to_csv("performance_metrics.csv")

