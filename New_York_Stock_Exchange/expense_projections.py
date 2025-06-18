import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

# Load the dataset
try:
    aapl = pd.read_csv('AAPL_full_forecasts.csv')
    aapl['Date'] = pd.to_datetime(aapl['Date'])  # Convert to datetime
    
    # Ensure we have the required columns
    required_cols = ['Date', 'Cost of Revenue', 'Research and Development', 'Gross Profit']
    missing_cols = [col for col in required_cols if col not in aapl.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

     
    # Prepare time series data
    aapl_ts = aapl.set_index('Date')['Gross Profit'].dropna()
    
    # ARIMA Model
    arima_model = ARIMA(aapl_ts, order=(1,1,1))
    arima_results = arima_model.fit()
    arima_forecast = arima_results.get_forecast(steps=4)
    
    # Prophet Model
    prophet_df = aapl_ts.reset_index()
    prophet_df.columns = ['ds', 'y']
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=4, freq='Q')
    prophet_forecast = m.predict(future)
    
    # expence_projections
    
    # Prepare data for R&D vs Revenue regression
    valid_data = aapl.dropna(subset=['Research and Development', 'Gross Profit'])
    X = valid_data[['Gross Profit']].values
    y = valid_data['Research and Development'].values
    
    if len(X) > 1:  # Need at least 2 samples for regression
        # Linear Regression Model
        rd_model = LinearRegression()
        rd_model.fit(X, y)
        
        # Predict future R&D
        future_revenue = np.array([500000, 550000, 600000]).reshape(-1, 1)
        future_rd = rd_model.predict(future_revenue)
        print("\nPredicted R&D Expenses:", future_rd)
    else:
        print("\nInsufficient data for R&D regression model")
    
    # COGS Ratio Analysis
    aapl['COGS_Ratio'] = aapl['Cost of Revenue'] / aapl['Gross Profit']
    avg_cogs_ratio = aapl['COGS_Ratio'].mean()
    print(f"\nAverage COGS Ratio: {avg_cogs_ratio:.2f}")
    

    # Visualization
    
    plt.figure(figsize=(12, 6))
    
    # Historical Gross Profit
    plt.plot(aapl_ts.index, aapl_ts, label='Historical Gross Profit', color='blue')
    
    # ARIMA Forecast
    arima_dates = pd.date_range(start=aapl_ts.index[-1], periods=5, freq='Q')[1:]
    plt.plot(arima_dates, arima_forecast.predicted_mean, 
             label='ARIMA Forecast', color='red', linestyle='--')
    
    # Prophet Forecast
    prophet_future = prophet_forecast[prophet_forecast['ds'] > aapl_ts.index[-1]]
    plt.plot(prophet_future['ds'], prophet_future['yhat'], 
             label='Prophet Forecast', color='green', linestyle='-.')
    
    plt.title('AAPL Gross Profit Forecasts')
    plt.xlabel('Date')
    plt.ylabel('Gross Profit ($)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
except FileNotFoundError:
    print("Error: File 'AAPL_full_forecasts.csv' not found.")
except Exception as e:
    print(f"\nAn error occurred: {str(e)}")

# save the results
try:
    forecasts = pd.DataFrame({
        'Date': arima_dates,
        'ARIMA_Forecast': arima_forecast.predicted_mean,
        'Prophet_Forecast': prophet_future['yhat'].values if not prophet_future.empty else np.nan
    })
    
    # Save to CSV
    forecasts.to_csv('AAPL_expense_projections.csv', index=False)
    print("\nExpense projections saved to 'AAPL_expense_projections.csv'")
except Exception as e:
    print(f"\nAn error occurred while saving the results: {str(e)}")