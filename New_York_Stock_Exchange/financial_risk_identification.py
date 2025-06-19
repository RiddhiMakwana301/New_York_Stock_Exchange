import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')

# Calculate Altman Z-Score (bankruptcy risk predictor)
fundamentals_merged['Working Capital'] = fundamentals_merged['Total Current Assets'] - fundamentals_merged['Total Current Liabilities']
fundamentals_merged['Retained Earnings'] = fundamentals_merged['Retained Earnings'].fillna(0)
fundamentals_merged['EBIT'] = fundamentals_merged['Earnings Before Interest and Tax']

# Calculate Altman Z-Score components carefully (handle division by zero)
fundamentals_merged['Altman_Z'] = (
    1.2 * (fundamentals_merged['Working Capital'] / fundamentals_merged['Total Assets'].replace(0, np.nan)) +
    1.4 * (fundamentals_merged['Retained Earnings'] / fundamentals_merged['Total Assets'].replace(0, np.nan)) +
    3.3 * (fundamentals_merged['EBIT'] / fundamentals_merged['Total Assets'].replace(0, np.nan)) +
    0.6 * (fundamentals_merged['Total Equity'] / fundamentals_merged['Total Liabilities'].replace(0, np.nan)) +
    1.0 * (fundamentals_merged['Total Revenue'] / fundamentals_merged['Total Assets'].replace(0, np.nan))
)

# Flag high-risk companies (Z-Score < 1.8 indicates distress)
high_risk = fundamentals_merged[fundamentals_merged['Altman_Z'] < 1.8].copy()
print(f"{len(high_risk)} companies in financial distress")

# Calculate Debt-to-Equity ratio (using Long-Term Debt and Total Equity)
fundamentals_merged['Debt_to_Equity'] = (
    fundamentals_merged['Long-Term Debt'] / 
    fundamentals_merged['Total Equity'].replace(0, np.nan)  # Handle division by zero
)

# Calculate Interest Coverage Ratio (EBIT / Interest Expense)
fundamentals_merged['Interest_Coverage'] = (
    fundamentals_merged['Earnings Before Interest and Tax'] / 
    fundamentals_merged['Interest Expense'].replace(0, np.nan)
)

# Companies with dangerous debt levels
debt_risks = fundamentals_merged[
    (fundamentals_merged['Debt_to_Equity'] > 2) | 
    (fundamentals_merged['Interest_Coverage'] < 2)  # EBIT/Interest < 2x is risky
][['Ticker Symbol', 'Security', 'Debt_to_Equity', 'Interest_Coverage']]

# Store the results
high_risk.to_csv('high_risk_companies.csv', index=False)
debt_risks.to_csv('debt_risks.csv', index=False)

print("High-risk companies saved to 'high_risk_companies.csv'")
print("Debt risk companies saved to 'debt_risks.csv'")

# Additional risk metrics
print("\nAdditional Risk Metrics:")
print(f"Average Debt-to-Equity Ratio: {fundamentals_merged['Debt_to_Equity'].mean():.2f}")
print(f"Companies with negative equity: {len(fundamentals_merged[fundamentals_merged['Total Equity'] < 0])}")

# make visualizations risk identification
# Debt-to-Equity ratio distribution
plt.figure(figsize=(10, 6))
plt.hist(fundamentals_merged['Debt_to_Equity'].dropna(), bins=30, color='green', alpha=0.7)
plt.title('Distribution of Debt-to-Equity Ratios')
plt.xlabel('Debt-to-Equity Ratio')
plt.ylabel('Frequency')
plt.axvline(x=2, color='red', linestyle='--', label='High Risk Threshold (D/E > 2)')
plt.legend()
plt.savefig('debt_to_equity_distribution.png')
plt.show()

# Interest Coverage Ratio distribution
plt.figure(figsize=(10, 6))
plt.hist(fundamentals_merged['Interest_Coverage'].dropna(), bins=30, color='orange', alpha=0.7)
plt.title('Distribution of Interest Coverage Ratios')
plt.xlabel('Interest Coverage Ratio')
plt.ylabel('Frequency')
plt.axvline(x=2, color='red', linestyle='--', label='Low Coverage Threshold (IC < 2)')
plt.legend()
plt.savefig('interest_coverage_distribution.png')  
plt.show()

