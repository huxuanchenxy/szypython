# 非阻塞模块
import sys
import os
import datetime
import random
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv3 import MySQLConnector
# 亲测可用


now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'tongjicar.log'
logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


try:
    start_time = datetime.datetime(2022, 9, 9, 0, 0, 0)
    end_time = datetime.datetime(2022, 9, 9, 23, 59, 59)
    interval = datetime.timedelta(minutes=3)

    current_time = start_time
    while current_time <= end_time:
        print(current_time.strftime("%Y-%m-%d %H:%M:%S"))
        if current_time.minute in [0, 6, 9, 12]:
            current_time += interval
        else:
            current_time += datetime.timedelta(minutes=3)
        random_number = random.randint(40, 75)
        print(random_number)
        mysql_connector1 = MySQLConnector('47.101.220.2','root', 'yfzx.2021',3306, 'aisense')
        sql1 = " INSERT INTO `aisense`.`g40_info`(`road_part`, `camera`, `time`, `carcount`, `timespan`) VALUES (28, 'K35+520', '{}', {}, 180);".format(current_time,random_number)
        mysql_connector1.execute_insert(sql1)
        print("insert g40_info sql ", sql1)

except Exception as e:
    print(e)
    logging.info('数据库插入报错:{}'.format(e))




