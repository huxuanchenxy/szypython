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
fname = now.strftime('%Y-%m-%d') + 'weather2.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
data = [{
      "cityid": 24,
      "parentid": 0,
      "citycode": "101020100",
      "city": "上海"
    },{
	"cityid": 2702,
	"parentid": 24,
	"citycode": "101021300",
	"city": "长宁区"
}, {
	"cityid": 2704,
	"parentid": 24,
	"citycode": "101020200",
	"city": "闵行区"
}, {
	"cityid": 2705,
	"parentid": 24,
	"citycode": "101021200",
	"city": "徐汇区"
}, {
	"cityid": 2706,
	"parentid": 24,
	"citycode": "101020600",
	"city": "浦东新区"
}, {
	"cityid": 2707,
	"parentid": 24,
	"citycode": "101021700",
	"city": "杨浦区"
}, {
	"cityid": 2708,
	"parentid": 24,
	"citycode": "101021500",
	"city": "普陀区"
}, {
	"cityid": 2709,
	"parentid": 24,
	"citycode": "101021400",
	"city": "静安区"
}, {
	"cityid": 2711,
	"parentid": 24,
	"citycode": "101021600",
	"city": "虹口区"
}, {
	"cityid": 2712,
	"parentid": 24,
	"citycode": "101020400",
	"city": "黄浦区"
}, {
	"cityid": 2714,
	"parentid": 24,
	"citycode": "101020900",
	"city": "松江区"
}, {
	"cityid": 2715,
	"parentid": 24,
	"citycode": "101020500",
	"city": "嘉定区"
}, {
	"cityid": 2716,
	"parentid": 24,
	"citycode": "101020300",
	"city": "宝山区"
}, {
	"cityid": 2717,
	"parentid": 24,
	"citycode": "101020800",
	"city": "青浦区"
}, {
	"cityid": 2718,
	"parentid": 24,
	"citycode": "101020700",
	"city": "金山区"
}, {
	"cityid": 2719,
	"parentid": 24,
	"citycode": "101021000",
	"city": "奉贤区"
}, {
	"cityid": 2720,
	"parentid": 24,
	"citycode": "101021100",
	"city": "崇明区"
}]

def getWeather(citycode):
    host = 'https://jisutqybmf.market.alicloudapi.com'
    path = '/weather/query'
    method = 'GET'
    appcode = 'a6cd0c215cf8468fa516a399da2bdc25'
    querys = 'city=&citycode={}&cityid=&ip=&location=location'.format(citycode)
    bodys = {}
    url = host + path + '?' + querys

    headers = {
    'Authorization': 'APPCODE ' + appcode
    }

    response = requests.request("GET", url, headers=headers)
    return response.text

def insertDB(citycode):
    try:
        ret = getWeather(citycode)
        now = datetime.datetime.now()
        mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx@2024', 3306,'aisense')
        sql = (" INSERT INTO `aisense`.`weather`(`areacode`, `value`, `date1`) VALUES ('{}', '{}', '{}') ".format(citycode,ret,now))

        ida = mysql_connector.execute_insert(sql)
        print("insert weather sql id", ida)
        logging.info("insert weather sql id {} ".format(ida))
        time.sleep(20)
    except Exception as e:
            print("Failed to getWeather {}".format(e))
            logging.error("Failed to getWeather {}".format(e))

def listCity():
    for item in data:
        citycode = item["citycode"]
        city = item["city"]
        print(city)
        logging.info("city {} ".format(city))
        insertDB(citycode)
    # insertDB('101021700')

while True:
    try:
        listCity()
    except Exception as e:
        logging.error(e)
    time.sleep(60*10)



