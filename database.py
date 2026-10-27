import sqlite3
import pandas as pd

conn = sqlite3.connect("financial_data.db")

df = pd.read_csv("data/processed_data.csv")

df.to_sql("stock_prices", conn, if_exists="replace", index=False)

print("Data stored in database.")

conn.close()