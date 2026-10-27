import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.graph_objects as go
from pipeline import run_pipeline

st.set_page_config(layout="wide")



st.title("📊 Financial Risk Monitoring Dashboard")

# Load data
data = run_pipeline()

# Show raw data
st.subheader("Price Data")
st.write(data.tail())

# 📊 Price with signals
st.subheader("📊 Price with Trade Signals")

fig = go.Figure()

# Price line
fig.add_trace(go.Scatter(
    x=data.index,
    y=data["Close"],
    name="Price"
))

# LONG signals (green)
longs = data[data["position"] == 1]
fig.add_trace(go.Scatter(
    x=longs.index,
    y=longs["Close"],
    mode='markers',
    name="LONG (Buy)",
    marker=dict(color="green", size=6)
))

# SHORT signals (red)
shorts = data[data["position"] == -1]
fig.add_trace(go.Scatter(
    x=shorts.index,
    y=shorts["Close"],
    mode='markers',
    name="SHORT (Sell)",
    marker=dict(color="red", size=6)
))

st.plotly_chart(fig)

# Volatility
st.subheader("Volatility Monitor")
st.line_chart(data["volatility"])

# 📈 Strategy vs Market
st.subheader("📈 Strategy vs Buy & Hold")
st.line_chart(data[["strategy_cum_returns", "buy_hold"]])

# 📊 Metrics
st.subheader("📊 Strategy Summary")

total_return = data["strategy_cum_returns"].iloc[-1] - 1
buy_hold_return = data["buy_hold"].iloc[-1] - 1

st.write(f"Strategy Return: {total_return:.2%}")
st.write(f"Buy & Hold Return: {buy_hold_return:.2%}")

# ⚠️ Anomalies
st.subheader("Risk Alerts")
anomalies = data[abs(data["zscore"]) > 3]

if len(anomalies) > 0:
    st.warning("⚠️ Anomalies detected!")
    st.write(anomalies[["Close", "returns", "zscore"]])
else:
    st.success("✅ No anomalies detected")

# 📥 Download
csv = data.to_csv().encode("utf-8")

st.download_button(
    label="📥 Download Report",
    data=csv,
    file_name="risk_report.csv",
    mime="text/csv",
)