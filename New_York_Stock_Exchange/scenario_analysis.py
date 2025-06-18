import pandas as pd

fixed_costs = 120000  # Example fixed operating costs
avg_cogs_ratio = 0.65  # Example: 65% average cost of goods sold ratio
contribution_margin = 1 - avg_cogs_ratio
break_even = fixed_costs / contribution_margin
print(f"Break-even revenue: ${break_even:,.2f}")

# Test impact of 10% cost increase
rev_scenarios = [500000, 550000, 600000]
cost_increase = 1.10  # 10% higher COGS

results = []
for rev in rev_scenarios:
    original_profit = rev * (1 - avg_cogs_ratio) - fixed_costs
    new_profit = rev * (1 - avg_cogs_ratio * cost_increase) - fixed_costs
    results.append({
        'Revenue': rev,
        'Original Profit': original_profit,
        'New Profit': new_profit,
        'Impact': new_profit - original_profit
    })

# Display results
df = pd.DataFrame(results)
df['Impact'] = df['Impact'].apply(lambda x: f"${x:,.2f}")
print(df)

# Save results to CSV
df.to_csv('scenario_analysis_results.csv', index=False)
print("Scenario analysis results saved to 'scenario_analysis_results.csv'")