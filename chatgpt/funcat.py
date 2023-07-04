from funcat import *
# from funcat.data.tushare import TushareDataBackend
# from funcat.data.tushare_backend import TushareDataBackend
# from funcat.data.rqalpha_data_backend import RQAlphaDataBackend
from funcat.helper import select

# 设置数据源
# set_data_backend(TushareDataBackend())

# 设置时间
T("20230601")

# 选股策略
select(
    lambda : CROSS(L, MA(L, 30)),
    start_date=20230601,
    end_date=20230626
)