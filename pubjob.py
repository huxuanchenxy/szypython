# encoding: utf-8
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


class Device:
    name = 'mydevice'
    time = datetime.now()



HOST = "47.101.220.2"
PORT = 1883
topic = "/water/control"

def test():
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(client_id)
    client.connect(HOST, PORT)

    dev1 = Device()
    dev1.name = 'step1'
    dev1.time = datetime.now()
    jsonstr = json.dumps(dev1.__dict__, default=str)
    client.publish(topic,jsonstr,0)
    print("第一步：", datetime.now())
    time.sleep(10)


    client_id2 = f'python-mqtt-{random.randint(0, 1000)}'
    client2 = mqtt.Client(client_id2)
    client2.connect(HOST, PORT)

    dev2 = Device()
    dev2.name = 'step2'
    dev2.time = datetime.now()
    jsonstr2 = json.dumps(dev2.__dict__, default=str)
    client2.publish(topic,jsonstr2,0)
    print("第二步：", datetime.now())
    #client.loop_forever()

def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    scheduler.add_job(test, 'interval', minutes=2)
    #scheduler.add_job(test, CronTrigger.from_crontab('0 0/2 * * *'))
    #scheduler.add_job(test, 'cron', day_of_week='*', hour='*', minute='2')
    scheduler.start()

if __name__ == '__main__':
    dojob()