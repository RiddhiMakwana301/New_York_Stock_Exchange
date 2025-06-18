import pandas as pd

# Load your data (replace with your actual data loading code)
fundamentals = pd.read_csv('fundamentals.csv')  # or from SQL, etc.

# Profitability Ratios
fundamentals['Gross Margin'] = (fundamentals['Total Revenue'] - fundamentals['Cost of Revenue']) / fundamentals['Total Revenue']
fundamentals['Operating Margin'] = fundamentals['Operating Income'] / fundamentals['Total Revenue']
fundamentals['Net Profit Margin'] = fundamentals['Net Income'] / fundamentals['Total Revenue']

# Liquidity Ratios
fundamentals['Current Ratio'] = fundamentals['Total Current Assets'] / fundamentals['Total Current Liabilities']
fundamentals['Quick Ratio'] = (fundamentals['Total Current Assets'] - fundamentals['Inventory']) / fundamentals['Total Current Liabilities']

# Leverage Ratios
fundamentals['Debt to Equity'] = fundamentals['Total Liabilities'] / fundamentals['Total Equity']
fundamentals['Debt Ratio'] = fundamentals['Total Liabilities'] / fundamentals['Total Assets']

# Efficiency Ratios
fundamentals['Asset Turnover'] = fundamentals['Total Revenue'] / fundamentals['Total Assets']
fundamentals['Inventory Turnover'] = fundamentals['Cost of Revenue'] / fundamentals['Inventory']

# Save the results
fundamentals.to_csv('fundamentals_with_ratios.csv', index=False)

print(fundamentals.columns.tolist())