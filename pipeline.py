import pandas as pd
import numpy as np
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_data():
    print("Loading data from CSV...")

    file_path = os.path.join(DATA_DIR, "processed_data.csv")

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Convert to numeric
    cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def clean_data(df):
    df = df.dropna()
    df = df.drop_duplicates()
    return df


def feature_engineering(df):
    print("Creating financial indicators...")

    # Returns
    df["returns"] = df["Close"].pct_change()

    # Moving averages
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    # Volatility
    df["volatility"] = df["returns"].rolling(20).std()

    # Z-score
    mean = df["returns"].mean()
    std = df["returns"].std()
    df["zscore"] = (df["returns"] - mean) / std

    # 📊 Market regime
    df["trend"] = np.where(df["MA20"] > df["MA50"], "Bullish", "Bearish")

    # 📉 Low risk condition
    vol_threshold = df["volatility"].quantile(0.2)
    df["low_risk"] = df["volatility"] < vol_threshold

    # 🎯 Position: LONG / SHORT / NONE
    df["position"] = np.where(
        (df["trend"] == "Bullish") & (df["low_risk"]),
        1,
        np.where(
            (df["trend"] == "Bearish") & (df["low_risk"]),
            -1,
            0
        )
    )

    # 📈 Strategy returns
    df["strategy_returns"] = df["position"] * df["returns"]

    # 📊 Cumulative returns
    df["strategy_cum_returns"] = (1 + df["strategy_returns"]).cumprod()

    # 📊 Buy & Hold
    df["buy_hold"] = (1 + df["returns"]).cumprod()

    df = df.dropna()

    return df


def run_pipeline():
    df = load_data()
    df = clean_data(df)
    df = feature_engineering(df)
    return df


if __name__ == "__main__":
    data = run_pipeline()
    print(data.tail())