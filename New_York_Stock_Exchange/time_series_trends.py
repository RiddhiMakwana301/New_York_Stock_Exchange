import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load and prepare data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')

# Convert and validate dates
fundamentals_merged['Period Ending'] = pd.to_datetime(fundamentals_merged['Period Ending'], errors='coerce')
fundamentals_merged = fundamentals_merged.dropna(subset=['Period Ending'])

# Data validation
required_columns = {
    'financial': ['Net Income', 'Total Revenue', 'Total Equity', 'Long-Term Debt', 
                 'Total Current Assets', 'Total Current Liabilities', 'Gross Profit'],
    'metadata': ['GICS Sector', 'Ticker Symbol', 'Security']
}

for col_type, cols in required_columns.items():
    missing = [col for col in cols if col not in fundamentals_merged.columns]
    if missing:
        raise ValueError(f"Missing {col_type} columns: {', '.join(missing)}")

# Calculate financial ratios with error handling
def safe_divide(a, b):
    return np.where(b != 0, a/b, np.nan)

fundamentals_merged['Net Margin'] = safe_divide(fundamentals_merged['Net Income'], fundamentals_merged['Total Revenue'])
fundamentals_merged['ROE'] = safe_divide(fundamentals_merged['Net Income'], fundamentals_merged['Total Equity'])
fundamentals_merged['Debt-to-Equity'] = safe_divide(fundamentals_merged['Long-Term Debt'], fundamentals_merged['Total Equity'])
fundamentals_merged['Current Ratio'] = safe_divide(fundamentals_merged['Total Current Assets'], 
                                                 fundamentals_merged['Total Current Liabilities'])
fundamentals_merged['Gross Margin'] = safe_divide(fundamentals_merged['Gross Profit'], 
                                               fundamentals_merged['Total Revenue'])

# Sector analysis with more metrics
sector_metrics = fundamentals_merged.groupby('GICS Sector').agg({
    'Net Margin': ['mean', 'median', 'std'],
    'ROE': ['mean', 'median'],
    'Debt-to-Equity': ['mean', 'median'],
    'Current Ratio': 'mean',
    'Gross Margin': 'mean',
    'Ticker Symbol': 'nunique'  # Count of unique companies
}).round(3)

# Rename columns for clarity
sector_metrics.columns = ['_'.join(col).strip() for col in sector_metrics.columns.values]
sector_metrics = sector_metrics.rename(columns={'Ticker Symbol_nunique': 'Company Count'})
sector_metrics.to_csv('sector_analysis_detailed.csv')

# Visualization
plt.figure(figsize=(15, 10))

# 1. Net Margin by Sector (updated to avoid deprecation warning)
plt.subplot(2, 2, 1)
sns.barplot(data=fundamentals_merged, y='GICS Sector', x='Net Margin', 
            estimator=np.median, errorbar=None, hue='GICS Sector', legend=False, palette='viridis')
plt.title('Median Net Margin by Sector', fontsize=12)
plt.xlabel('Net Margin (%)')
plt.ylabel('')

# 2. Debt-to-Equity Distribution (updated to avoid deprecation warning)
plt.subplot(2, 2, 2)
sns.boxplot(data=fundamentals_merged, y='GICS Sector', x='Debt-to-Equity',
           showfliers=False, hue='GICS Sector', legend=False, palette='plasma')
plt.title('Debt-to-Equity Ratio Distribution', fontsize=12)
plt.xlabel('Debt-to-Equity Ratio')
plt.ylabel('')
plt.xlim(0, 5)  # Limit x-axis for better visualization

# 3. ROE vs Net Margin Scatter
plt.subplot(2, 2, 3)
sns.scatterplot(data=fundamentals_merged, x='Net Margin', y='ROE', 
               hue='GICS Sector', alpha=0.6, s=100)
plt.title('ROE vs Net Margin by Sector', fontsize=12)
plt.xlabel('Net Margin (%)')
plt.ylabel('Return on Equity (%)')
plt.axhline(0, color='grey', linestyle='--')
plt.axvline(0, color='grey', linestyle='--')

# 4. Current Ratio Heatmap
plt.subplot(2, 2, 4)
sector_pivot = fundamentals_merged.pivot_table(values='Current Ratio', 
                                             index='GICS Sector',
                                             aggfunc='median')
sns.heatmap(sector_pivot, annot=True, fmt='.1f', cmap='YlOrRd', cbar=False)
plt.title('Median Current Ratio by Sector', fontsize=12)
plt.ylabel('')

plt.tight_layout()
plt.savefig('sector_financial_analysis.png', dpi=300)
plt.show()

# Additional Analysis: Top/Bottom Performers (updated to not require tabulate)
top_companies = fundamentals_merged.groupby(['Ticker Symbol', 'Security', 'GICS Sector'])\
    .agg({'Net Margin': 'median', 'ROE': 'median'})\
    .sort_values('Net Margin', ascending=False)

print("\nTop 10 Companies by Net Margin:")
print(top_companies.head(10))

print("\nBottom 10 Companies by Net Margin:")
print(top_companies.tail(10))