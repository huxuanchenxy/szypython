import efinance as ef
import pandas as pd

# 定义一个函数来检查是否出现“大长腿”下引线
def is_long_legged_doji(df):
    # “大长腿”下引线的定义：实体部分较小，下影线较长
    # print(df)
    return df['收盘'].iloc[-1] - df['开盘'].iloc[-1] < df['最低'].iloc[-1] - df['收盘'].iloc[-1]

# 获取A股的股票列表
# stocks_df = ef.stock.get_stock_codes()
# stocks = stocks_df['600000'].tolist()
stocks = ['600029', '000663', '600848']

# 存储出现“大长腿”下引线的股票
long_legged_doji_stocks = []

for stock in stocks:
    # 获取股票的历史数据
    df = ef.stock.get_quote_history(stock)
    
    # 检查是否出现“大长腿”下引线
    if is_long_legged_doji(df):
        long_legged_doji_stocks.append(stock)

# 打印出现“大长腿”下引线的股票
print(long_legged_doji_stocks)