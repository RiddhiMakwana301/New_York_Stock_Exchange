import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Project free cash flows (simplified)
projected_cash_flows = [25000, 30000, 35000, 40000]  # Example projections
discount_rate = 0.10  # 10% discount rate

# Calculate present value
dcf_value = sum(
    cf / (1 + discount_rate) ** (i+1) 
    for i, cf in enumerate(projected_cash_flows)
)


# adding revenue data from AAPl_full_forecasts.csv
aapl_forecast = pd.read_csv('AAPl_full_forecasts.csv')
aapl_revenue = aapl_forecast['Cost of Revenue'].dropna().values

# Simulate revenue with uncertainty
n_simulations = 1000
rev_mean = aapl_revenue.mean()
rev_std = aapl_revenue.std()

simulated_rev = np.random.normal(rev_mean, rev_std, n_simulations)
prob_above_target = np.mean(simulated_rev > 600000)  # P(Revenue > $600k)

# Display results
print(f"Discounted Cash Flow Value: ${dcf_value:,.2f}")
print(f"Probability of Revenue > $600k: {prob_above_target:.2%}")