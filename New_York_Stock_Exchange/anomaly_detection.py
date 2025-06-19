import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
from sklearn.ensemble import IsolationForest
from mpl_toolkits.mplot3d import Axes3D

fundamentals_merged = pd.read_csv('merged_fundamentals_securities.csv')

# Calculate Net Margin if not present
fundamentals_merged['Net Margin'] = fundamentals_merged['Net Income'] / fundamentals_merged['Total Revenue']

# Calculate Debt-to-Equity ratio
fundamentals_merged['Debt-to-Equity'] = fundamentals_merged['Long-Term Debt'] / fundamentals_merged['Total Equity']

# Verify Current Ratio exists (it does in your data)
print("Current Ratio" in fundamentals_merged.columns)  # Should return True

# Select only rows where all required ratios exist
X = fundamentals_merged[['Net Margin', 'Current Ratio', 'Debt-to-Equity']].dropna()

# Proceed with Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# Add results to dataframe
fundamentals_merged.loc[X.index, 'Anomaly_Score'] = model.decision_function(X)
fundamentals_merged.loc[X.index, 'Is_Anomaly'] = model.predict(X)

# Show top anomalies
anomalies = fundamentals_merged[fundamentals_merged['Is_Anomaly'] == -1]
print(f"Found {len(anomalies)} anomalous companies")


# Visualize anomalies in 3D space
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot normal points
normal = fundamentals_merged[fundamentals_merged['Is_Anomaly'] == 1]
ax.scatter(
    normal['Net Margin'],
    normal['Current Ratio'],
    normal['Debt-to-Equity'],
    c='blue',
    label='Normal'
)

# Plot anomalies
ax.scatter(
    anomalies['Net Margin'],
    anomalies['Current Ratio'],
    anomalies['Debt-to-Equity'],
    c='red',
    label='Anomaly'
)

ax.set_xlabel('Net Margin')
ax.set_ylabel('Current Ratio')
ax.set_zlabel('Debt-to-Equity')
plt.title('Financial Anomalies in 3D Space')
plt.legend()
plt.savefig('financial_anomalies_3d.png')
plt.show()

# Display key info about anomalies
anomaly_report = anomalies[[
    'Ticker Symbol', 
    'Security',
    'GICS Sector',
    'Net Margin',
    'Current Ratio',
    'Debt-to-Equity',
    'Total Revenue'
]].sort_values('Net Margin')

print(anomaly_report.head(10))
# Save anomalies to CSV
anomaly_report.to_csv('financial_anomalies_report.csv', index=False)
# Save the updated fundamentals data with anomaly scores
fundamentals_merged.to_csv('fundamentals_with_anomalies.csv', index=False)
print("Anomaly detection completed and results saved.")