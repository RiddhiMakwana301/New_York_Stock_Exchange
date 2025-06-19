import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the merged fundamentals and securities data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')  
fundamentals_merged['Period Ending'] = pd.to_datetime(fundamentals_merged['Period Ending'], errors='coerce')

# Data validation
if 'GICS Sector' not in fundamentals_merged.columns:
    raise ValueError("The 'GICS Sector' column is missing from the merged DataFrame.")

required_columns = ['Net Income', 'Total Revenue', 'Total Equity', 'Long-Term Debt']
for col in required_columns:
    if col not in fundamentals_merged.columns:
        raise ValueError(f"The required column '{col}' is missing from the merged DataFrame.")

# Calculate financial ratios
fundamentals_merged['Net Margin'] = fundamentals_merged['Net Income'] / fundamentals_merged['Total Revenue']
fundamentals_merged['ROE'] = fundamentals_merged['Net Income'] / fundamentals_merged['Total Equity']
fundamentals_merged['Debt-to-Equity'] = fundamentals_merged['Long-Term Debt'] / fundamentals_merged['Total Equity']

# Sector analysis
sector_analysis = fundamentals_merged.groupby('GICS Sector').agg({
    'Net Margin': 'mean',
    'ROE': 'mean',
    'Debt-to-Equity': 'mean'  
}).reset_index()

# Rename columns for output
sector_analysis.columns = ['GICS Sector', 'Average Net Margin', 'Average ROE', 'Average Debt-to-Equity']
sector_analysis.to_csv('sector_analysis.csv', index=False)
print("Sector-wise financial analysis saved to 'sector_analysis.csv'")

# Visualization
plt.figure(figsize=(10, 6))
sns.barplot(data=sector_analysis, y='GICS Sector', x='Average Net Margin')
plt.title('Average Net Margin by Sector', fontsize=14)
plt.xlabel('Net Margin (%)', fontsize=12)
plt.ylabel('Sector', fontsize=12)
plt.tight_layout()
plt.show()