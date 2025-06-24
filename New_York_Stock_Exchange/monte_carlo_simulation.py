import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Generate 10,000 simulated revenue outcomes from a normal distribution
np.random.seed(42)
base_revenue = 1_000_000
volatility = 0.15
simulations = pd.DataFrame({
    'Scenario': np.random.normal(base_revenue, base_revenue*volatility, 10000)
})

# Calculate confidence intervals
lower_90 = np.percentile(simulations['Scenario'], 5)
upper_90 = np.percentile(simulations['Scenario'], 95)
mean_revenue = simulations['Scenario'].mean()

# calculate the standard deviation
std_dev_revenue = simulations['Scenario'].std()

# add date column
simulations['Date'] = pd.date_range(start='2023-01-01', periods=10000, freq='D')
# add mean and confidence intervals to the DataFrame with different values
simulations['Mean'] = mean_revenue
simulations['Lower 90% CI'] = lower_90
simulations['Upper 90% CI'] = upper_90
simulations['Standard Deviation'] = std_dev_revenue

# profit and loss calculation by GSCI sector
# Assuming you have a DataFrame with GSCI sector data, from securities
# For simplicity, let's assume the GSCI sector is a column in the simulations DataFrame
simulations['GSCI Sector'] = np.random.choice(['Energy', 'Materials', 'Industrials', 'Consumer Discretionary', 'Consumer Staples', 'Health Care', 'Financials', 'Information Technology', 'Telecommunication Services', 'Utilities'], size=10000)
# Calculate profit and loss based on the base revenue
simulations['GSCI Sector Profit'] = simulations.groupby('GSCI Sector')['Scenario'].transform(lambda x: x - base_revenue)
simulations['GSCI Sector Loss'] = simulations.groupby('GSCI Sector')['Scenario'].transform(lambda x: base_revenue - x)



# save the results in cvs file
save_path = 'monte_carlo_simulation_results.csv'
simulations.to_csv(save_path, index=False)
print(f"Monte Carlo simulation results saved to {save_path}")