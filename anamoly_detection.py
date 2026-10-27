import pandas as pd
import numpy as np

print("Running anomaly detection...")

# load dataset
df = pd.read_csv("data/processed_data.csv")

# keep only numeric columns
numeric_df = df.select_dtypes(include=[np.number])

# choose the first numeric column for analysis
prices = numeric_df.iloc[:, 0]

# calculate statistics
mean = prices.mean()
std = prices.std()

# compute z-score
z_scores = (prices - mean) / std

# detect anomalies
outliers = df[np.abs(z_scores) > 3]

print("\nAnomalies detected:\n")
print(outliers)