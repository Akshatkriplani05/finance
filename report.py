import pandas as pd

df = pd.read_csv("data/processed_data.csv")

print("Data Summary")
print(df.describe())

print("\nTop 5 rows")
print(df.head())