import pandas as pd
import load_data as ld

# Clean fundamentals Table
fundamentals = ld.fundamentals.rename(columns={'Unnamed: 0': 'id'})
fundamentals.dropna(subset=['Net Income', 'Total Revenue'], inplace=True)

# FIX: Use pd.to_datetime instead of ld.to_datetime
fundamentals['Period Ending'] = pd.to_datetime(fundamentals['Period Ending'], errors='coerce')

# Clean securities Table
ld.securities['Ticker symbol'] = ld.securities['Ticker symbol'].str.upper()
securities = ld.securities[['Ticker symbol', 'Security', 'GICS Sector', 'GICS Sub Industry']].copy()

# Clean prices-split-adjusted Table
# FIX: Column name should be 'date' not 'Date' (as per your dataset description)
ld.price_split['date'] = pd.to_datetime(ld.price_split['date'], errors='coerce')

# Filter for relevant tickers
valid_tickers = fundamentals['Ticker Symbol'].unique()
price_split = ld.price_split[ld.price_split['symbol'].isin(valid_tickers)].copy()

# Print success message
print("Data cleaning completed successfully!")
print(f"Fundamentals shape: {fundamentals.shape}")
print(f"Prices split-adjusted shape: {price_split.shape}")