import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')
sector_analysis = pd.read_csv('sector_analysis.csv')

# Print columns for debugging
print("\nColumns in fundamentals_merged:", fundamentals_merged.columns.tolist())
print("\nColumns in sector_analysis:", sector_analysis.columns.tolist())

# 1. Analyze high debt companies (using original data)
if 'Long-Term Debt' in fundamentals_merged.columns and 'Total Equity' in fundamentals_merged.columns:
    fundamentals_merged['Debt-to-Equity'] = fundamentals_merged['Long-Term Debt'] / fundamentals_merged['Total Equity']
    high_debt = fundamentals_merged[fundamentals_merged['Debt-to-Equity'] > 2]  # Threshold = 2
    
    if not high_debt.empty:
        print("\nCompanies with high debt-to-equity (>2):")
        print(high_debt[['Ticker Symbol', 'Security', 'Debt-to-Equity']].drop_duplicates())
    else:
        print("\nNo companies found with debt-to-equity > 2")
else:
    print("\nRequired columns for debt analysis missing in fundamentals_merged")

# 2. Analyze income drops (using original data)
if 'Net Income' in fundamentals_merged.columns and 'Ticker Symbol' in fundamentals_merged.columns:
    fundamentals_merged = fundamentals_merged.sort_values(['Ticker Symbol', 'Period Ending'])
    fundamentals_merged['Net Income Growth'] = fundamentals_merged.groupby('Ticker Symbol')['Net Income'].pct_change()
    income_drops = fundamentals_merged[fundamentals_merged['Net Income Growth'] < -0.3]  # >30% drop
    
    if not income_drops.empty:
        print("\nCompanies with significant income drops (>30%):")
        print(income_drops[['Ticker Symbol', 'Security', 'Period Ending', 'Net Income', 'Net Income Growth']])
    else:
        print("\nNo companies found with >30% income drops")
else:
    print("\nRequired columns for income analysis missing in fundamentals_merged")

# 3. Visualizations (using sector analysis)
plt.figure(figsize=(12, 6))
sns.boxplot(data=sector_analysis, y='Average Debt-to-Equity', palette='coolwarm')
plt.title('Sector-Wise Debt-to-Equity Ratio Distribution', fontsize=14)
plt.ylabel('Average Debt-to-Equity Ratio', fontsize=12)
plt.tight_layout()
plt.savefig('sector_debt_to_equity_distribution.png') 
plt.show()

# Save results
if 'high_debt' in locals() and not high_debt.empty:
    high_debt.to_csv('high_debt_companies.csv', index=False)
if 'income_drops' in locals() and not income_drops.empty:
    income_drops.to_csv('income_drops_companies.csv', index=False)

print("\nAnalysis complete. Results saved to CSV files where applicable.")