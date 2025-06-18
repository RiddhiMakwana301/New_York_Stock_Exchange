import pandas as pd

# Load all tables
fundamentals = pd.read_csv("fundamentals.csv")
prices = pd.read_csv("prices.csv")
price_split = pd.read_csv("prices-split-adjusted.csv")
securities = pd.read_csv("securities.csv")

print(fundamentals.head())  # Check structure