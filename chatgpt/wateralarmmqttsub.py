# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

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
from mysqlhelper import Database



db = Database(host='47.101.220.2', user='root', password='yfzx.2021', db='aisense')
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ecgs")

def on_message(client, userdata, msg):
    try:
        print(msg.topic+" "+str(msg.payload))

        msgb = msg.payload
        msgstr = msgb.decode("utf-8")
        jsonobj = json.loads(msgstr)
        # print(jsonobj)
        
        doalarm(jsonobj)
    except Exception as e:
        print("Error processing message: ", e)

def doalarm(jsonobj):
    try:
        print("do alarm")

        # Execute a query to select data from a table
        # query = " SELECT * FROM water_alarm_set "
        # cursor.execute(query)
        sql = " SELECT * FROM water_alarm_set "
        rows = db.select(sql)
        print("sql",sql)
        # print(rows)
        # print(rows[1])
        # row = rows[1]
        # print(row[1])
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in rows:
            print(row)
            alarmkey = row[1]
            limitup = row[2]
            limitdown = row[3]
            alarmvalue = ""
            flagup = False
            flagdown = False
            if(alarmkey == "cl"):
                alarmvalue = jsonobj["cl"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("cl too high",alarmvalue,limitup)
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("cl too low",alarmvalue,flagdown)
            if(alarmkey == "orp"):
                alarmvalue = jsonobj["orp"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("orp too high",alarmvalue,limitup)
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("orp too low",alarmvalue,limitdown)
            if(alarmkey == "ph"):
                alarmvalue = jsonobj["ph"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("ph too high",alarmvalue,limitup)
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("ph too low",alarmvalue,limitdown)
            if(alarmkey == "temp"):
                alarmvalue = jsonobj["temp"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("temp too high",alarmvalue,limitup)
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("temp too low",alarmvalue,limitdown)
            if(alarmkey == "turb"):
                alarmvalue = jsonobj["turb"]
                if(alarmvalue > limitup):
                    flagup = True
                    print("turb too high",alarmvalue,limitup)
                if(alarmvalue < limitdown):
                    flagdown = True
                    print("turb too low",alarmvalue,limitdown)
            if alarmvalue != "":
                if flagup == True:
                        sql = ("INSERT INTO `aisense`.`water_alarm2`(`device_id`, `alarmkey`, `alarmvalue`, `alarmdes`, `alarmstatus`, `date1`) VALUES (%s, %s, %s, %s, %s, %s)")
                        data = (jsonobj["id"], alarmkey, alarmvalue, "超出上限", 1, current_time)
                        id = db.insert(sql, data)
                        print("insert sql id ", id)
                if flagdown == True:
                        sql = ("INSERT INTO `aisense`.`water_alarm2`(`device_id`, `alarmkey`, `alarmvalue`, `alarmdes`, `alarmstatus`, `date1`) VALUES (%s, %s, %s, %s, %s, %s)")
                        data = (jsonobj["id"], alarmkey, alarmvalue, "超出下限", 1, current_time)
                        id = db.insert(sql, data)
                        print("insert sql id ", id)
    except Exception as e:
        print("Error alarm processing message: ", str(e))

# MQTT服务器的地址和端口
broker_address = "47.101.220.2"
broker_port = 1883

# MQTT客户端的ID和心跳包间隔时间（以秒为单位）
client_id = f'python-mqtt-{random.randint(0, 1000)}'
keep_alive_interval = 60

# 定义MQTT客户端对象并设置心跳包间隔时间
client = mqtt.Client(client_id=client_id)
client.keep_alive = keep_alive_interval

# 定义连接断开的回调函数
def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with code: " + str(rc))
    # 如果连接断开，尝试重新连接
    while rc != 0:
        try:
            rc = client.reconnect()
            print("Reconnected to MQTT broker with code: " + str(rc))
            client.subscribe("ecgs")
        except:
            print("Failed to reconnect to MQTT broker")
            time.sleep(60*3)

# 设置连接断开的回调函数
client.on_disconnect = on_disconnect

client.on_connect = on_connect
client.on_message = on_message

# 连接到MQTT服务器
print("Connecting to MQTT broker...")
client.connect(broker_address, broker_port)
client.loop_start()

# doalarm({})

# 每隔10秒发送一次心跳包
while True:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    echomsg = ("{} Sending heartbeat...").format(current_time)
    print(echomsg)
    client.publish("heartbeat", "alive")
    time.sleep(60*3)

