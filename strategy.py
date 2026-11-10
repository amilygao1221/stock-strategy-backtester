
import pandas as pd
import matplotlib.pyplot as plt

# Load historical stock data
data = pd.read_csv(
    "aapl_data.csv",
    index_col=0,
    parse_dates=True
)

# Calculate moving averages
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()

# Generate trading signals
data["Signal"] = (
    data["SMA_20"] > data["SMA_50"]
).astype(int)

# Identify changes in position
data["Trade"] = data["Signal"].diff().fillna(0)

print(data[
    ["Close", "SMA_20", "SMA_50", "Signal", "Trade"]
].tail(10))

# Plot price and moving averages
plt.figure(figsize=(11, 6))

plt.plot(
    data.index,
    data["Close"],
    label="AAPL Adjusted Close",
    alpha=0.6
)

plt.plot(
    data.index,
    data["SMA_20"],
    label="SMA 20"
)

plt.plot(
    data.index,
    data["SMA_50"],
    label="SMA 50"
)

plt.title("AAPL Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Adjusted Price (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("moving_averages.png", dpi=200)
plt.show()
