# 620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7
import tushare as ts
import datetime
# # 设置Tushare的Token
# ts.set_token('620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7')

# # 初始化Tushare接口
# pro = ts.pro_api()
stock_list = []
with open('code9.txt', 'r') as file:
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
ts.set_token('620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7')
# pro = ts.pro_api('620b7be5808cc3232cf02770bb01981fe86ffb9293a6f8fe595d9fc7')

# 初始化Tushare接口
pro = ts.pro_api()

# 获取近一周内的日期范围
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

# 获取A股股票列表
# stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')

# 遍历股票列表，筛选出近一周内出现缺口的股票
gapped_stocks = []
for code in stock_list:
    # if req <= 499
    # 获取近一周的交易数据
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    if len(df) >= 2:
        # 计算缺口大小（当天开盘价 - 前一天收盘价），并判断是否为向上缺口
        gap_size = df.iloc[0]['open'] - df.iloc[1]['close']
        if gap_size > 0:
            gapped_stocks.append((code))

# 输出筛选结果
for stock in gapped_stocks:
    print(stock)

