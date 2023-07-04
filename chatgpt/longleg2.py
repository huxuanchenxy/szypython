import requests
import pandas as pd

# Define a function to check if a stock has a long-legged doji
def is_long_legged_doji(df):
    return df['close'].iloc[-1] - df['open'].iloc[-1] < df['low'].iloc[-1] - df['close'].iloc[-1]

# Your IEX Cloud API key
api_key = 'pk_5d3592b7a5854077abced0d855b61a91'

# List of A-share stocks
# This is just an example, in reality you need to get all A-share stock codes
# stocks = ['AAPL', 'MSFT', 'GOOGL']
stocks = ['600000']

# Store stocks with long-legged doji
long_legged_doji_stocks = []

for stock in stocks:
    # Get the stock's historical data
    response = requests.get(f'https://cloud.iexapis.com/stable/stock/{stock}/chart/1d?token={api_key}')
    data = response.json()
    df = pd.DataFrame(data)
    
    # Check if the stock has a long-legged doji
    if is_long_legged_doji(df):
        long_legged_doji_stocks.append(stock)

# Print stocks with long-legged doji
print(long_legged_doji_stocks)