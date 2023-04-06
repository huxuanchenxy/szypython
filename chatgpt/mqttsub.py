# Welcome to Cursor



# 1. Try generating with command K on a new line. Ask for a pytorch script of a feedforward neural network
# 2. Then, select the outputted code and hit chat. Ask if there's a bug. Ask how to improve.
# 3. Try selecting some code and hitting edit. Ask the bot to add residual layers.
# 4. To try out cursor on your own projects, go to the file menu (top left) and open a folder.

import paho.mqtt.client as mqtt
import mysql.connector
import json
import random
import time
import datetime

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ecgs")

def on_message(client, userdata, msg):
    try:
        print(msg.topic+" "+str(msg.payload))
        # Connect to the database
        cnx = mysql.connector.connect(user='root', password='yfzx.2021',
                                    host='47.101.220.2',
                                    database='aisense')
        cursor = cnx.cursor()

        # Insert some data into the table
        msgb = msg.payload
        msgstr = msgb.decode("utf-8")
        jsonobj = json.loads(msgstr)
        # print(jsonobj)
        add_data = ("INSERT INTO `aisense`.`water`(`device_id`, `ec`, `o2`, `orp`, `ph`, `temp`, `tub`, `date1`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        data = (jsonobj["id"], jsonobj["ec"], jsonobj["cl"], jsonobj["orp"], jsonobj["ph"], jsonobj["temp"], jsonobj["turb"], jsonobj["timestamp"])
        cursor.execute(add_data, data)

        # Make sure data is committed to the database
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()
    except Exception as e:
        print("Error processing message: ", e)



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

# 每隔10秒发送一次心跳包
while True:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    echomsg = ("{} Sending heartbeat...").format(current_time)
    print(echomsg)
    client.publish("heartbeat", "alive")
    time.sleep(60*3)

