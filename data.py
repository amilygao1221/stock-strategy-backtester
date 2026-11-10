
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Choose a stock
ticker = "AAPL"

# Download historical stock prices
data = yf.download(
    ticker,
    start="2020-01-01",
    end="2026-01-01",
    auto_adjust=True,
    progress=False
)

# Check whether data was downloaded successfully
if data.empty:
    raise ValueError("No stock data downloaded.")
# Flatten MultiIndex columns
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Sort by date
data = data.sort_index()

# Display the first five rows
print("First five rows:")
print(data.head())

# Display basic information
print("\nDataset shape:")
print(data.shape)

print("\nColumn names:")
print(data.columns)

# Calculate daily returns
data["Daily_Return"] = data["Close"].pct_change()
data.to_csv("aapl_data.csv")

print("\nDaily returns:")
print(data[["Close", "Daily_Return"]].head())



# Plot historical closing prices
plt.figure(figsize=(10, 5))

plt.plot(data.index, data["Close"], label="AAPL Adjusted Close")

plt.xlabel("Date")
plt.ylabel("Adjusted Price (USD)")
plt.title("Apple Historical Stock Prices (2020–2025)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("aapl_price_history.png", dpi=200)
plt.show()
