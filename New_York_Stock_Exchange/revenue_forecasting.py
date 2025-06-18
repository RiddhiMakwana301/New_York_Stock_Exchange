import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load your revenue forecast data
try:
    forecasts = pd.read_csv('AAPL_revenue_forecasts.csv')
    print("Data loaded successfully. First few rows:")
    print(forecasts.head())
    
    # Check if we have the expected forecast columns
    if 'ARIMA_Forecast' not in forecasts.columns:
        raise ValueError("ARIMA_Forecast column not found in the data")

    # Generate synthetic expense data based on typical Apple ratios
    # Apple's typical COGS ratio: ~58%, R&D ratio: ~6% (adjust as needed)
    forecasts['Cost of Revenue'] = forecasts['ARIMA_Forecast'] * 0.58
    forecasts['Research and Development'] = forecasts['ARIMA_Forecast'] * 0.06
    forecasts['Operating Expenses'] = forecasts['ARIMA_Forecast'] * 0.12  # Additional ops expenses
    
    # Calculate key metrics
    forecasts['Gross Profit'] = forecasts['ARIMA_Forecast'] - forecasts['Cost of Revenue']
    forecasts['Operating Income'] = forecasts['Gross Profit'] - forecasts['Operating Expenses']
    forecasts['Gross Margin'] = forecasts['Gross Profit'] / forecasts['ARIMA_Forecast']
    forecasts['Operating Margin'] = forecasts['Operating Income'] / forecasts['ARIMA_Forecast']
    
    # Expense Ratio Analysis
    forecasts['COGS_Ratio'] = forecasts['Cost of Revenue'] / forecasts['ARIMA_Forecast']
    avg_cogs_ratio = forecasts['COGS_Ratio'].mean()
    
    # Linear Regression for R&D (using time as predictor)
    forecasts['Period'] = np.arange(len(forecasts))  # Create time periods
    
    X = forecasts[['Period']].values
    y = forecasts['Research and Development'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 3 periods
    future_periods = np.array([[len(forecasts)], [len(forecasts)+1], [len(forecasts)+2]])
    future_rd = model.predict(future_periods)
    
    # Visualization
    plt.figure(figsize=(12, 6))
    
    # Revenue and Expenses
    plt.subplot(1, 2, 1)
    plt.plot(forecasts['Date'], forecasts['ARIMA_Forecast'], label='Revenue')
    plt.plot(forecasts['Date'], forecasts['Cost of Revenue'], label='COGS')
    plt.plot(forecasts['Date'], forecasts['Operating Expenses'], label='Op Expenses')
    plt.title('Revenue and Expenses Projection')
    plt.xticks(rotation=45)
    plt.legend()
    
    # Margins
    plt.subplot(1, 2, 2)
    plt.plot(forecasts['Date'], forecasts['Gross Margin'], label='Gross Margin')
    plt.plot(forecasts['Date'], forecasts['Operating Margin'], label='Operating Margin')
    plt.title('Profit Margins')
    plt.xticks(rotation=45)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('financial_forecasts.png', bbox_inches='tight')
    plt.show()
    
    # Print key results
    print("\nKey Financial Metrics:")
    print(f"Average COGS Ratio: {avg_cogs_ratio:.2%}")
    print(f"Average Gross Margin: {forecasts['Gross Margin'].mean():.2%}")
    print("\nR&D Expense Projections:")
    for i, rd in enumerate(future_rd, 1):
        print(f"Period {i}: ${rd:,.2f}")
    
    # Save results
    forecasts.to_csv('AAPL_full_forecasts.csv', index=False)
    print("\nResults saved to 'AAPL_full_forecasts.csv'")

except FileNotFoundError:
    print("Error: 'AAPL_revenue_forecasts.csv' not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")