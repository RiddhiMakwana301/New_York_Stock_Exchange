import pandas as pd
import load_data as ld
fundamentals_merged = pd.merge(
    ld.fundamentals,
    ld.securities,
    left_on='Ticker Symbol',
    right_on='Ticker symbol',
    how='left'
)

# store the merged DataFrame in a file
fundamentals_merged.to_csv('merged_fundamentals_securities.csv', index=False)
print("Merged fundamentals and securities data saved to 'merged_fundamentals_securities.csv'")