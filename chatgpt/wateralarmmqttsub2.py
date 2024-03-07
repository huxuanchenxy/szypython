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
# sys.path.append("F:/netcontrol/project/2022/python/")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv2 import MySQLConnector

# 断线重连相关配置 
reconnect_interval = 30  # 3秒重连间隔
reconnect_tries = 10000    # 最大重连次数
now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'wateralarmmqttsub2.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
# db = Database(host='47.101.220.2', user='root', password='yfzx@2024', db='aisense')



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    logging.info("Connected with result code {}".format(str(rc)))
    client.subscribe("ecgs")

def on_message(client, userdata, msg):
    try:
        print(msg.topic+" "+str(msg.payload))
        logging.info(msg.topic+" "+str(msg.payload))
        msgb = msg.payload
        msgstr = msgb.decode("utf-8")
        jsonobj = json.loads(msgstr)
        # print(jsonobj)
        
        doalarm(jsonobj)
    except Exception as e:
        print("Error processing message: ", e)
        logging.error("Error processing message:{}".format(e))

def doalarm(jsonobj):
    try:
        print("jsonobj",jsonobj)
        logging.info("jsonobj",jsonobj)
        mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx@2024', 'aisense')
        print("do alarm")
        logging.info("do alarm")
        # Execute a query to select data from a table
        # query = " SELECT * FROM water_alarm_set "
        # cursor.execute(query)
        sql = " SELECT * FROM water_alarm_set "
        # print("readytosql",sql)
        # rows = db.select(sql)
        rows = mysql_connector.execute_query(sql)
        # print("sql",sql)
        # print(rows)
        # print(rows[1])
        # row = rows[1]
        # print(row[1])
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in rows:
            # print(row)
            alarmkey = row[1]
            limitup = row[2]
            limitdown = row[3]
            alarmvalue = ""
            flagup = False
            flagdown = False
            # if(alarmkey == "cl"):
            #     alarmvalue = jsonobj["cl"]
            #     if(alarmvalue > limitup):
            #         flagup = True
            #         print("cl too high",alarmvalue,limitup)
            #         logging.info("cl too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
            #     if(alarmvalue < limitdown):
            #         flagdown = True
            #         print("cl too low",alarmvalue,limitdown)
            #         logging.info("cl too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
            if(alarmkey == "orp"):
                alarmvalue = jsonobj["orp"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("orp too high",alarmvalue,limitup)
                    logging.info("orp too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("orp too low",alarmvalue,limitdown)
                    logging.info("orp too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
            if(alarmkey == "ph"):
                alarmvalue = jsonobj["ph"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("ph too high",alarmvalue,limitup)
                    logging.info("ph too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("ph too low",alarmvalue,limitdown)
                    logging.info("ph too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
            if(alarmkey == "temp"):
                alarmvalue = jsonobj["temp"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("temp too high",alarmvalue,limitup)
                    logging.info("temp too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("temp too low",alarmvalue,limitdown)
                    logging.info("temp too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
            if(alarmkey == "turb"):
                alarmvalue = jsonobj["turb"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("turb too high",alarmvalue,limitup)
                    logging.info("turb too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("turb too low",alarmvalue,limitdown)
                    logging.info("turb too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
            if alarmvalue != "":
                if flagup == True:
                        sql = ("INSERT INTO `aisense`.`water_alarm2`(`device_id`, `alarmkey`, `alarmvalue`, `alarmdes`, `alarmstatus`, `date1`) VALUES (%s, %s, %s, %s, %s, %s)")
                        data = (jsonobj["id"], alarmkey, alarmvalue, "超出上限", 1, current_time)
                        # id = db.insert(sql, data)
                        id = mysql_connector.execute_insert(sql, data)
                        print("insert sql id", id)
                        logging.info("insert sql id {}".format(id))
                if flagdown == True:
                        sql = ("INSERT INTO `aisense`.`water_alarm2`(`device_id`, `alarmkey`, `alarmvalue`, `alarmdes`, `alarmstatus`, `date1`) VALUES (%s, %s, %s, %s, %s, %s)")
                        data = (jsonobj["id"], alarmkey, alarmvalue, "超出下限", 1, current_time)
                        # id = db.insert(sql, data)
                        id = mysql_connector.execute_insert(sql, data)
                        print("insert sql id", id)
                        logging.info("insert sql id {}".format(id))
    except Exception as e:
        print("Error alarm processing message: ", str(e))
        logging.error("Error alarm processing message:{} ".format(str(e)))

# MQTT服务器的地址和端口
broker_address = "47.101.220.2"
broker_port = 1883

# MQTT客户端的ID和心跳包间隔时间（以秒为单位）
client_id = f'python-mqtt-{random.randint(0, 1000)}'
keep_alive_interval = 60*60*24*365

# 定义MQTT客户端对象并设置心跳包间隔时间
client = mqtt.Client(client_id=client_id)
client.keep_alive = keep_alive_interval
client.reconnect_delay_set(reconnect_interval, reconnect_tries) 
# 定义连接断开的回调函数
def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with code: " + str(rc))
    logging.info("Disconnected from MQTT broker with code: {}".format(str(rc)))
    # 如果连接断开，尝试重新连接
    while rc != 0:
        try:
            rc = client.reconnect()
            print("Reconnected to MQTT broker with code: " + str(rc))
            logging.info("Reconnected to MQTT broker with code: {}".format(str(rc)))
            client.subscribe("ecgs")
        except Exception as e:
            print("Failed to reconnect to MQTT broker",e)
            logging.error("Failed to reconnect to MQTT broker {}".format(e))
            time.sleep(60*3)

# 设置连接断开的回调函数
client.on_disconnect = on_disconnect

client.on_connect = on_connect
client.on_message = on_message

# 连接到MQTT服务器
print("Connecting to MQTT broker...")
logging.info("Connecting to MQTT broker...")
client.connect(broker_address, broker_port)
client.loop_start()
# client.loop_forever()
# doalarm({})

# 每隔10秒发送一次心跳包
while True:
    data = str(time.time())
    print('state: ', client._state, 'loop进程：', client._thread, end='  ')
    logging.info('state: {} loop thread： {}'.format(client._state, client._thread))
    # if client._state != 2:
    #     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     echomsg = ("{} \nSending heartbeat...").format(current_time)
    #     print(echomsg)
    #     logging.info(echomsg)
    #     client.publish("heartbeat", "alive")
    # else:
    #     print('\n客户端已断开。')
    #     logging.info('\n client is broken。')
    #     client.disconnect()
    #     print('\n手动断开')
    #     logging.info('\n manul off')
    #     client.loop_stop()
    #     print('\n手动loop_stop')
    #     logging.info('\n manul loop_stop')
    #     time.sleep(10)
    #     print('\n等待{}秒'.format(10))
    #     logging.info('\n wait {} s'.format(10))
    #     client.reconnect()
    #     print('\n手动reconnect')
    #     logging.info('\n manul reconnect')
    #     client.loop_start()
    #     print('\n手动loop_start')
    #     logging.info('\n manul loop_start')
    threadmsg = '{}'.format(client._thread)
    if threadmsg.find('stopped daemon') >= 0 or client._state == 2:
        print('\n客户端已断开。')
        logging.info(' client is broken。')
        client.disconnect()
        print('\n手动断开')
        logging.info(' manul off')
        client.loop_stop()
        print('\n手动loop_stop')
        logging.info(' manul loop_stop')
        time.sleep(10)
        print('\n等待{}秒'.format(10))
        logging.info(' wait {} s'.format(10))
        client.reconnect()
        print('\n手动reconnect')
        logging.info(' manul reconnect')
        client.loop_start()
        print('\n手动loop_start')
        logging.info(' manul loop_start')
    else :
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        echomsg = ("{} \nSending heartbeat...").format(current_time)
        print(echomsg)
        logging.info(echomsg)
        client.publish("heartbeat", "alive")
    # if count == 4:
    #     print('disconnect.................')
    #     # client.disconnect()
    #     # # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
    #     # # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
    #     # client.loop_stop()
    # if count == 8:
    #     print('尝试重连')
    #     # client.reconnect()  # 必须重连将 client._state 从断开状态切换为初始化状态
    #     # client.loop_start()
    #     count = 0
    # count += 1
    time.sleep(60*5)

