import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
ticker = "^GSPC"
start_date = "2025-01-20"  # Changed from 2025 to 2020 as future dates won't have data
interval = "1d"
try:
    # Download data
    data = yf.download(ticker, start=start_date, interval=interval)
    # Check if data is valid
    if data.empty:
        raise ValueError("No data fetched. Check ticker or internet connection.")
    # Choose appropriate column
    price_column = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    # Calculate percentage change
    first_price = data[price_column].iloc[0].item()
    last_price = data[price_column].iloc[-1].item()
    percent_change = ((last_price - first_price) / first_price) * 100
    # Determine color based on percentage change
    change_color = 'green' if percent_change >= 0 else 'red'
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data[price_column], label=f'S&P 500 {price_column}', color='blue')
    # Add percentage change annotation
    plt.annotate(f'{percent_change:.2f}%',
                xy=(data.index[-1], last_price),
                xytext=(data.index[-1], last_price * 1.05),
                fontsize=24,
                fontweight='bold',
                color=change_color)
    plt.title(f'S&P 500 {price_column} - From January 20, 2025 Onwards')  # Updated title to match new date
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")
