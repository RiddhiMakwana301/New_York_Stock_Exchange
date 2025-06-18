import pandas as pd

# Load the datasets (replace paths with your actual files)
fundamentals = pd.read_csv("fundamentals.csv")
prices = pd.read_csv("prices-split-adjusted.csv")
securities = pd.read_csv("securities.csv")

# Clean fundamentals: Rename the first column
fundamentals = fundamentals.rename(columns={fundamentals.columns[0]: 'id'})

# Convert date columns to datetime
fundamentals['Period Ending'] = pd.to_datetime(fundamentals['Period Ending'])
prices['date'] = pd.to_datetime(prices['date'])

# Merge fundamentals with securities
fundamentals_merged = pd.merge(
    fundamentals,
    securities,
    left_on='Ticker Symbol',
    right_on='Ticker symbol',
    how='left'
)

# Link stock prices to fundamentals (on Ticker + Date)
merged_data = pd.merge(
    fundamentals_merged,
    prices,
    left_on=['Ticker Symbol', 'Period Ending'],
    right_on=['symbol', 'date'],
    how='left'  # Keeps all financials, even if no price data exists
)

# Save the merged data
merged_data.to_csv("fundamentals_with_prices.csv", index=False)
print("Merged data saved to 'fundamentals_with_prices.csv'")