import yfinance as yf
import pandas as pd

# List of stock tickers to monitor.
stocks = ['PAGP', 'NOG', 'STNG']

def alert(stock, current_price, sma, direction):
    print(f"Alert: {stock} Price {direction} Crossover")
    print(f"{stock} has crossed {direction} its 20-day SMA.")
    print(f"Current Price: {current_price:.2f}")
    print(f"20-day SMA: {sma:.2f}")
    print('----------------------')

def get_scalar(val):
    # If val is a Series (single element), return its first element as a float.
    if isinstance(val, pd.Series):
        return float(val.iloc[0])
    return float(val)

def check_stock(stock):
    # Download approximately one month of daily data.
    data = yf.download(stock, period="30d", interval="1d")
    if len(data) < 20:
        print(f"Not enough data for {stock}")
        return

    # Calculate the 20-day Simple Moving Average (SMA)
    data['SMA20'] = data['Close'].rolling(window=20).mean()

    # Ensure we have at least 2 days to compare (yesterday and today)
    if len(data) < 2:
        return

    # Retrieve the last two days for crossover detection.
    yesterday = data.iloc[-2]
    today = data.iloc[-1]

    # Use get_scalar to avoid FutureWarning when converting to float.
    close_yesterday = get_scalar(yesterday['Close'])
    sma_yesterday   = get_scalar(yesterday['SMA20'])
    close_today     = get_scalar(today['Close'])
    sma_today       = get_scalar(today['SMA20'])

    # Check for upward crossover: yesterday's close was at or below SMA and today's close is above SMA.
    if close_yesterday <= sma_yesterday and close_today > sma_today:
        alert(stock, close_today, sma_today, "Upward")
    # Check for downward crossover: yesterday's close was at or above SMA and today's close is below SMA.
    elif close_yesterday >= sma_yesterday and close_today < sma_today:
        alert(stock, close_today, sma_today, "Downward")
    else:
        print(f"No crossover detected for {stock}")

def main():
    for stock in stocks:
        check_stock(stock)

if __name__ == '__main__':
    main()