import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# Load merged fundamentals data
fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')

# CALCULATE REQUIRED METRICS FROM EXISTING COLUMNS
# Calculate Working Capital (Current Assets - Current Liabilities)
fundamentals_merged['Working Capital'] = fundamentals_merged['Total Current Assets'] - fundamentals_merged['Total Current Liabilities']

# Calculate Net Margin if not exists
if 'Net Margin' not in fundamentals_merged.columns:
    fundamentals_merged['Net Margin'] = fundamentals_merged['Net Income'] / fundamentals_merged['Total Revenue']

# Calculate Debt-to-Equity if not exists
if 'Debt-to-Equity' not in fundamentals_merged.columns:
    fundamentals_merged['Debt-to-Equity'] = fundamentals_merged['Long-Term Debt'] / fundamentals_merged['Total Equity']

# Calculate Current Ratio if not exists
if 'Current Ratio' not in fundamentals_merged.columns:
    fundamentals_merged['Current Ratio'] = fundamentals_merged['Total Current Assets'] / fundamentals_merged['Total Current Liabilities']

# CALCULATE ALTMAN Z-SCORE (BANKRUPTCY RISK)
fundamentals_merged['Altman_Z'] = (
    1.2 * (fundamentals_merged['Working Capital'] / fundamentals_merged['Total Assets']) +
    1.4 * (fundamentals_merged['Retained Earnings'] / fundamentals_merged['Total Assets']) +
    3.3 * (fundamentals_merged['Earnings Before Interest and Tax'] / fundamentals_merged['Total Assets']) +
    0.6 * (fundamentals_merged['Total Equity'] / fundamentals_merged['Total Liabilities']) +
    1.0 * (fundamentals_merged['Total Revenue'] / fundamentals_merged['Total Assets'])
)

# ANOMALY DETECTION

# Select only numerical columns that exist in the dataframe
available_columns = [col for col in ['Net Margin', 'Current Ratio', 'Debt-to-Equity'] 
                    if col in fundamentals_merged.columns]

if len(available_columns) >= 2:  # Need at least 2 features for anomaly detection
    X = fundamentals_merged[available_columns].dropna()
    
    if not X.empty:
        model = IsolationForest(contamination=0.05, random_state=42)
        fundamentals_merged.loc[X.index, 'Anomaly_Score'] = model.fit_predict(X)
        fundamentals_merged['Is_Anomaly'] = np.where(fundamentals_merged['Anomaly_Score'] == -1, 1, 0)
    else:
        fundamentals_merged['Is_Anomaly'] = 0
else:
    fundamentals_merged['Is_Anomaly'] = 0

# RISK SCORING SYSTEM
conditions = [
    (fundamentals_merged['Altman_Z'] < 1.8),
    (fundamentals_merged['Debt-to-Equity'] > 2),
    (fundamentals_merged['Is_Anomaly'] == 1)
]
choices = [10, 7, 5]  # Risk points
fundamentals_merged['Risk_Score'] = np.select(conditions, choices, default=0)

fundamentals_merged['Risk_Level'] = pd.cut(
    fundamentals_merged['Risk_Score'],
    bins=[-1, 3, 7, 20],
    labels=['Low', 'Medium', 'High']
)

# SAVE RESULTS
fundamentals_merged.to_csv('fundamentals_with_risk_scores.csv', index=False)

print("Risk assessment completed successfully!")
print("\nRisk Level Distribution:")
print(fundamentals_merged['Risk_Level'].value_counts())

print("\nSample of High Risk Companies:")
print(fundamentals_merged[fundamentals_merged['Risk_Level'] == 'High'][['Ticker Symbol', 'Security', 'Risk_Score']].head())