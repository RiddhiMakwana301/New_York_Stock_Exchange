import pandas as pd

# Load data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')

# Calculate Required Metrics First 

# 1. Calculate Revenue Growth (quarter-over-quarter)
fundamentals_merged['Revenue_Growth'] = fundamentals_merged.groupby('Ticker Symbol')['Total Revenue'].pct_change()

# 2. Calculate Inventory Change
fundamentals_merged['Inventory_Change'] = fundamentals_merged.groupby('Ticker Symbol')['Inventory'].pct_change()

# Risk Detection 

# A. Inventory Risks (growing inventory despite low revenue growth)
inventory_risks = fundamentals_merged[
    (fundamentals_merged['Inventory_Change'] > 0.3) & 
    (fundamentals_merged['Revenue_Growth'] < 0.1)
]

# B. Cash Flow Issues (profitable but negative operating cash flow)
cash_flow_issues = fundamentals_merged[
    (fundamentals_merged['Net Income'] > 0) & 
    (fundamentals_merged['Net Cash Flow-Operating'] < 0)
]

# Save Results
inventory_risks.to_csv('inventory_risks.csv', index=False)
cash_flow_issues.to_csv('cash_flow_issues.csv', index=False)

print(f"Found {len(inventory_risks)} inventory risk cases")
print(f"Found {len(cash_flow_issues)} cash flow issues")