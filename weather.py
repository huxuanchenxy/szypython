import urllib, urllib3
import ssl
import requests
import datetime
import logging
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv3 import MySQLConnector

now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'weather.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

def getWeather():
    host = 'https://weather01.market.alicloudapi.com'
    path = '/area-to-weather'
    method = 'GET'
    appcode = 'a6cd0c215cf8468fa516a399da2bdc25'
    querys = 'areaCode=310000&needMoreDay=0&needIndex=0&needHourData=0&need3HourForcast=0&needAlarm=0&area=%E4%B8%BD%E6%B1%9F'
    bodys = {}
    url = host + path + '?' + querys

    headers = {
    'Authorization': 'APPCODE ' + appcode
    }

    response = requests.request("GET", url, headers=headers)
    return response.text

def insertDB():
    try:
        ret = getWeather()
        now = datetime.datetime.now()
        mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx@2024', 3306,'aisense')
        sql = (" INSERT INTO `aisense`.`weather`(`areacode`, `value`, `date1`) VALUES ('{}', '{}', '{}') ".format('310000',ret,now))

        ida = mysql_connector.execute_insert(sql)
        print("insert weather sql id", ida)
        logging.info("insert weather sql id {} ".format(ida))
    except Exception as e:
            print("Failed to getWeather {}".format(e))
            logging.error("Failed to getWeather {}".format(e))


while True:
    try:
        insertDB()
    except Exception as e:
        logging.error(e)
    time.sleep(60*5)



