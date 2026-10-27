import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Generating graphs...")

# load dataset
df = pd.read_csv("data/processed_data.csv")

# convert numeric columns properly
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df["MA_20"] = pd.to_numeric(df["MA_20"], errors="coerce")
df["MA_50"] = pd.to_numeric(df["MA_50"], errors="coerce")
df["Daily_Return"] = pd.to_numeric(df["Daily_Return"], errors="coerce")
df["Volatility"] = pd.to_numeric(df["Volatility"], errors="coerce")

# remove rows with NaN
df = df.dropna()

# -------- Price Trend --------
plt.figure()

plt.plot(df["Close"])

plt.title("Stock Price Trend")
plt.xlabel("Time")
plt.ylabel("Price")

plt.show()


# -------- Moving Average --------
plt.figure()

plt.plot(df["Close"], label="Close Price")
plt.plot(df["MA_20"], label="20 Day MA")
plt.plot(df["MA_50"], label="50 Day MA")

plt.legend()
plt.title("Moving Average Analysis")

plt.show()


# -------- Returns Distribution --------
plt.figure()

sns.histplot(df["Daily_Return"], bins=50)

plt.title("Distribution of Daily Returns")

plt.show()


# -------- Volatility --------
plt.figure()

plt.plot(df["Volatility"])

plt.title("Volatility Trend")
plt.xlabel("Time")
plt.ylabel("Volatility")

plt.show()