# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

import logging
import os
import sys
import paho.mqtt.client as mqtt
import mysql.connector
import json
import random
import time
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv3 import MySQLConnector


now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'waterzhaoteng.log'
logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

while True:
    data = str(time.time())
    print('start read zhaoteng db: {}'.format(now))
    logging.info('start read zhaoteng db:  {}'.format(now))
    mysql_connector = MySQLConnector('47.101.216.100','output', 'qaz123456',5559, 'server_mtw')
    sql = " SELECT siteNo,wrwdm,vtime,v FROM server_mtw.pwkwrwlist where siteNo='73639242018829' and wrwdm IN('B01','011','060') "
    # print(sql)
    rows = mysql_connector.execute_query(sql)
    # print(rows)
    v1 =0
    v3 = 0
    v4 = 0
    siteNo = ''
    res_date = ''
    for row in rows:
            siteNo = row[0]
            wrwdm = row[1]
            res_date = row[2]
            v = row[3]
            # v1 as COD,v3 as NH3,v4 as flow
            # [wrwdm]	[名称]	[单位]
            # 011	COD	mg/L
            # 060	氨氮	mg/L
            # B01	瞬时流量	0.1吨/秒
            if wrwdm == '011':
                  v1 = v
            if wrwdm == '060':
                  v3 = v    
            if wrwdm == 'B01':
                  v4 = v 
    try:
        mysql_connector1 = MySQLConnector('47.101.220.2','root', 'yfzx@2024',3306, 'server_mtw')
        sql1 = " INSERT INTO `server_mtw`.`pwkdata`(`siteNo`, `res_date`, `isupload`, `flag`, `v1`, `v2`, `v3`, `v4`, `v5`, `v6`, `v7`, `v8`, `v9`, `v10`, `v11`, `v12`, `v13`, `v14`, `v15`) VALUES ('{}', '{}', 0, 'N', {}, 0, {}, {}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); ".format(siteNo,res_date,v1,v3,v4)
        mysql_connector1.execute_insert(sql1)
        print("insert waterzhaoteng sql ", sql1)
        logging.info('insert waterzhaoteng sql :  {}'.format(sql1))
    except Exception as e:
        print("Error processing message: ", e)
        logging.error("Error processing message: {}".format(e))
    time.sleep(60*5)

