import pandas as pd
import sqlite3

# Load raw data
fundamentals = pd.read_csv("fundamentals.csv")
securities = pd.read_csv("securities.csv")
prices_split = pd.read_csv("prices-split-adjusted.csv")

# Clean fundamentals: Rename the first column
fundamentals = fundamentals.rename(columns={'Unnamed: 0': 'id'})

# Clean securities: Standardize ticker symbols
securities['Ticker symbol'] = securities['Ticker symbol'].str.upper()

# Merge fundamentals + securities - drop the duplicate column after merge
fundamentals_merged = pd.merge(
    fundamentals,
    securities,
    left_on='Ticker Symbol',
    right_on='Ticker symbol',
    how='left'
).drop(columns=['Ticker symbol'])  # Drop the duplicate column

# Store in SQLite database
conn = sqlite3.connect("nyse_finance.db")

# Write tables to SQL
fundamentals_merged.to_sql("fundamentals", conn, if_exists="replace", index=False)
securities.to_sql("securities", conn, if_exists="replace", index=False)
prices_split.to_sql("prices", conn, if_exists="replace", index=False)

conn.close()
print("Data successfully stored in SQLite database!")