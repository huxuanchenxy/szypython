# 620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7
import tushare as ts
import datetime
# # 设置Tushare的Token
# ts.set_token('620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7')

# # 初始化Tushare接口
# pro = ts.pro_api()
stock_list = []
with open('code.txt', 'r') as file:
    line = file.readline()
    line = line.replace(" ","")
    line = line.replace("\n","")
    if len(line) == 9:
        stock_list.append(line)
    while line:
        # print(line)
        line = file.readline()
        line = line.replace(" ","")
        line = line.replace("\n","")
        if len(line) == 9:
            stock_list.append(line)

# print(stock_list)
# 初始化pro接口
pro = ts.pro_api('620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7')

# pro = ts.pro_api()

# df = pro.daily(ts_code='000519.SZ', start_date='20230712', end_date='20230713')
# print(df)
# 获取昨天的日期
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
# yesterday = yesterday.replace("-","")
# print(yesterday)
# 获取A股股票列表
# stock_list = ts.get_stock_basics()
# df = pro.daily(ts_code='301393.SZ', start_date=yesterday, end_date=yesterday)
# print(df)
# 遍历股票列表，筛选出昨天出现向上缺口的股票
gapped_stocks = []
# for code, name in stock_list.iterrows():
i = 0
for code in stock_list:
    # 获取昨天的交易数据
    # df = ts.get_hist_data(code, start=yesterday, end=yesterday)
    if i > 1500 and i <= 2000:
        df = pro.daily(ts_code=code, start_date=yesterday, end_date=yesterday)
        # print(df)
        if df is not None and len(df) == 1:
            if df['open'][0] > df['close'][0] and df['open'][0] > df['high'][0]:
                # gapped_stocks.append((code, name['name']))
                gapped_stocks.append(code)
    i = i + 1

print(gapped_stocks)
# 输出筛选结果
# for stock in gapped_stocks:
#     print(stock)

