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
from mysqlhelperv2 import MySQLConnector

# 断线重连相关配置 
reconnect_interval = 3  # 3秒重连间隔
reconnect_tries = 10    # 最大重连次数
now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'watermqttsub.log'
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
        mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx@2024', 'aisense')
        print(msg.topic+" "+str(msg.payload))
        logging.info('receive:topic:{}payload:{}'.format(msg.topic,str(msg.payload)))
        # Connect to the database
        # cnx = mysql.connector.connect(user='root', password='yfzx@2024',
        #                             host='47.101.220.2',
        #                             database='aisense')
        # cursor = cnx.cursor()

        # Insert some data into the table
        msgb = msg.payload
        msgstr = msgb.decode("utf-8")
        jsonobj = json.loads(msgstr)
        # print(jsonobj)
        
        sql = 'INSERT INTO `aisense`.`water`(`device_id`, `ec`, `o2`, `orp`, `ph`, `temp`, `tub`, `date1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        data = (jsonobj["id"], -1, jsonobj["cl"], jsonobj["orp"], jsonobj["ph"], jsonobj["temp"], jsonobj["turb"], jsonobj["timestamp"])
        id = mysql_connector.execute_insert(sql, data)
        # id = db.insert(sql, data=(jsonobj["id"], jsonobj["ec"], jsonobj["cl"], jsonobj["orp"], jsonobj["ph"], jsonobj["temp"], jsonobj["turb"], jsonobj["timestamp"]))
        logging.info('water sql insert id {}'.format(id))
    except Exception as e:
        print("Error processing message: ", e)
        logging.error("Error processing message: {}".format(e))

# MQTT服务器的地址和端口
broker_address = "47.101.220.2"
broker_port = 1883

# MQTT客户端的ID和心跳包间隔时间（以秒为单位）
client_id = f'python-mqtt-{random.randint(0, 1000)}'
keep_alive_interval = 60

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
            # client = mqtt.Client(client_id=client_id)
            # client.connect(broker_address, broker_port)
            print("Reconnected to MQTT broker with code: " + str(rc))
            logging.info("Reconnected to MQTT broker with code: {}".format(str(rc)))
            client.loop_start()
            client.subscribe("ecgs")
        except Exception as e:
            print("Failed to reconnect to MQTT broker")
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
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    echomsg = ("{} Sending heartbeat...").format(current_time)
    print(echomsg)
    logging.info(echomsg)
    client.publish("heartbeat", "alive")
    time.sleep(60*3)

