from alpha_vantage.timeseries import TimeSeries
import pandas as pd

# https://www.alphavantage.co/support/#api-key
# 这个地方获取
ts = TimeSeries(key='AHOO0IKH1PRPRYRH')

# 定义一个函数来检查是否出现“大长腿”下引线
def is_long_legged_doji(df):
    # “大长腿”下引线的定义：实体部分较小，下影线较长
    return df['Close'].iloc[-1] - df['Open'].iloc[-1] < df['Low'].iloc[-1] - df['Close'].iloc[-1]

# Get daily data for a stock
data, meta_data = ts.get_daily(symbol='512010')
# 存储出现“大长腿”下引线的股票
long_legged_doji_stocks = []
# Check if the stock has a long-legged doji
if is_long_legged_doji(pd.DataFrame(data)):
    long_legged_doji_stocks.append('512010')