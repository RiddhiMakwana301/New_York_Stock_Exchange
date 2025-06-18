import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
prices_split = pd.read_csv("prices-split-adjusted.csv")
fundamentals = pd.read_csv("fundamentals.csv")
securities = pd.read_csv("securities.csv")

# Clean and merge data
fundamentals = fundamentals.rename(columns={'Unnamed: 0': 'id'})
fundamentals['Period Ending'] = pd.to_datetime(fundamentals['Period Ending'])
securities['Ticker symbol'] = securities['Ticker symbol'].str.upper()

fundamentals_merged = pd.merge(
    fundamentals,
    securities,
    left_on='Ticker Symbol',
    right_on='Ticker symbol',
    how='left'
)

# Get latest stock price and calculate ratios
latest_prices = prices_split.groupby('symbol').last().reset_index()

valuation = pd.merge(
    fundamentals_merged,
    latest_prices[['symbol', 'close']],
    left_on='Ticker Symbol',
    right_on='symbol',
    how='left'
)

valuation['PE Ratio'] = valuation['close'] / valuation['Earnings Per Share']
valuation['PB Ratio'] = valuation['close'] / (valuation['Total Equity'] / valuation['Estimated Shares Outstanding'])

# Remove extreme outliers for better visualization
valuation = valuation[(valuation['PE Ratio'] < 100) & (valuation['PB Ratio'] < 20)]

# ----------------------------------
# Visualization 1: P/E Ratio by Sector (Boxplot)
# ----------------------------------
plt.figure(figsize=(12, 6))
sns.boxplot(
    data=valuation,
    x='GICS Sector',
    y='PE Ratio',
    palette='viridis'
)
plt.title('P/E Ratio Distribution by Sector', fontsize=14)
plt.xlabel('Sector', fontsize=12)
plt.ylabel('Price-to-Earnings Ratio', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('pe_ratio_by_sector.png')  # Save as image
plt.show()

# ----------------------------------
# Visualization 2: P/B vs P/E (Scatter Plot)
# ----------------------------------
plt.figure(figsize=(12, 6))
scatter = sns.scatterplot(
    data=valuation,
    x='PE Ratio',
    y='PB Ratio',
    hue='GICS Sector',
    palette='tab20',
    s=100,
    alpha=0.7
)

# Add market average lines
plt.axvline(x=valuation['PE Ratio'].median(), color='red', linestyle='--', label='Median P/E')
plt.axhline(y=valuation['PB Ratio'].median(), color='blue', linestyle='--', label='Median P/B')

plt.title('P/B Ratio vs. P/E Ratio by Sector', fontsize=14)
plt.xlabel('Price-to-Earnings Ratio', fontsize=12)
plt.ylabel('Price-to-Book Ratio', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('pb_vs_pe_scatter.png')  # Save as image
plt.show()

# Save data
valuation.to_csv('valuation_analysis.csv', index=False)
print("Analysis saved to:")
print("- valuation_analysis.csv")
print("- pe_ratio_by_sector.png")
print("- pb_vs_pe_scatter.png")