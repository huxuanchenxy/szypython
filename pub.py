# encoding: utf-8
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json

class Device:
    name = 'mydevice'
    time = datetime.now()

dev1 = Device()
dev1.name = 'mydevice'
dev1.time = datetime.now()

HOST = "47.101.220.2"
PORT = 1883
topic = "/water/control"

def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    jsonstr = json.dumps(dev1.__dict__, default=str)
    client.publish(topic,jsonstr,0)
    print("第一步：", datetime.now())
    time.sleep(10)
    dev1.time = datetime.now()
    jsonstr = json.dumps(dev1.__dict__, default=str)
    client.publish(topic,jsonstr,0)
    print("第二步：", datetime.now())
    #client.loop_forever()

if __name__ == '__main__':
    test()