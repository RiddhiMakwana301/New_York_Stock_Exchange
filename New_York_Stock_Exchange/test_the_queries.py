import sqlite3
import pandas as pd

conn = sqlite3.connect("nyse_finance.db")

# Query 1: Apple's financials + stock price
query_apple = """
SELECT 
    f.[Ticker Symbol], f.[Period Ending], f.[Total Revenue], f.[Net Income], p.close as stock_price
FROM 
    fundamentals f
JOIN 
    prices p ON f.[Ticker Symbol] = p.symbol AND f.[Period Ending] = p.date
WHERE 
    f.[Ticker Symbol] = 'AAPL'
"""
df_apple = pd.read_sql(query_apple, conn)
print(df_apple.head())

# Query 2: Sector-wise revenue
query_sector = """
SELECT 
    s.[GICS Sector], 
    AVG(f.[Total Revenue]) as avg_revenue
FROM 
    fundamentals f
JOIN 
    securities s ON f.[Ticker Symbol] = s.[Ticker symbol]
GROUP BY 
    s.[GICS Sector]
"""
df_sector = pd.read_sql(query_sector, conn)
print(df_sector.head())

conn.close()