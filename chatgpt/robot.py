import datetime
import os
import socket
import sys
import time
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv2 import MySQLConnector
import requests
import xml.etree.ElementTree as ET
import json

now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'robot.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


def GetRobotRealTimeInfoResponse():
    url = "http://10.89.34.76:11456"

    payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:stat=\"http://tempuri.org/station.xsd\">\r\n    <soapenv:Header/>\r\n    <soapenv:Body>\r\n        <stat:GetRobotRealTimeInfo>\r\n            <RobotId>1</RobotId>\r\n        </stat:GetRobotRealTimeInfo>\r\n    </soapenv:Body>\r\n</soapenv:Envelope>"
    headers = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction': '""',
    'Content-Length': '304',
    'Host': '10.89.34.76:11456',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.5.5 (Java/12.0.1)'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    # dom = ET.fromstring(response.text)
    # print(dom)
    # names = dom.findall('jdata')
    # print(names)
    ret = getXml(response.text)
    dbInsert(ret)
    # logging.info(response.text)

def dbInsert(ret):
    if ret['Code'] == 0:
        print('Read xml success')
        TEM = ''
        HUM = ''
        CO = ''
        O2 = ''
        CH4 = ''
        PM25 = ''
        SMOKE = ''
        H2S = ''
        PM50 = ''
        PM25 = ''
        collectTime = ''
        rotationAngle = ''
        height = ''
        robotPositonX = ''
        robotPositonY = ''
        data = ret['Data']
        robotPositonX = data['robotPositon'][0]
        robotPositonY = data['robotPositon'][1]
        height = data['height']
        rotationAngle = data['rotationAngle']
        collectTime = data['collectTime']
        gasData = data['gasData']
        for obj in gasData:
            if obj['id'] == 1:
                TEM = obj['TEM']
            if obj['id'] == 2:
                HUM = obj['HUM']
            if obj['id'] == 3:
                CO = obj['CO']
            if obj['id'] == 5:
                O2 = obj['O2']
            if obj['id'] == 6:
                CH4 = obj['CH4']
            if obj['id'] == 8:
                PM25 = obj['PM25']
            if obj['id'] == 11:
                SMOKE = obj['SMOKE']
            if obj['id'] == 16:
                H2S = obj['H2S']
            if obj['id'] == 18:
                PM50 = obj['PM50']
        # print('co',CO)
        mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx.2021', 'aisense')
        sql = (" INSERT INTO `aisense`.`gasrobot`( `o2`, `h2s`, `co`, `ch4`, `co2`, `pm25`, `pm10`, `hum`, `pm50`, `tem`, `robotPositonX`, `robotPositonY`, `height`, `rotationAngle`, `smoke`, `date1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data = (   O2 ,  H2S ,  CO ,  CH4 ,  '' ,  PM25 ,  '' ,  HUM ,  PM50 ,  TEM ,  robotPositonX ,  robotPositonY ,  height ,  rotationAngle ,  SMOKE ,  collectTime  )
        ida = mysql_connector.execute_insert(sql, data)
        print("insert gas sql id", ida)
        logging.info("insert gas sql id {} ".format(ida))
        # print(PM50)

def getXml(xml):

    # root = ET.fromstring(xml) #获得根节点
    # jdata = root.findall('./{http://tempuri.org/station.xsd}jdata')[0]
    left = xml.find('<jdata>')
    left = left + 7
    # print(left)
    right = xml.find('</jdata>')
    # print(right)
    # right = root.find('</jdata>')
    jdata = xml[left:right]
    # print(jdata)
    # print(root[left,right])
    ret = json.loads(jdata)
    # print(ret['Code'])
    # print(data)
    # walkXml(root,resultList,'')

    return ret

while True:
    try:
        GetRobotRealTimeInfoResponse()
    except Exception as e:
        logging.error(e)
    time.sleep(60*5)