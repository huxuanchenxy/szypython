# encoding: utf-8
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json
from apscheduler.schedulers.background  import BlockingScheduler
import logging
from apscheduler.triggers.cron import CronTrigger


class Device01:
    A01 = 110000
    res = '123'

class Device02:
    A02 = 110000
    res = '123'

class Device03:
    A03 = 110000
    res = '123'

class Device04:
    A04 = 110000
    res = '123'

class Device06:
    A06 = 110000
    res = '123'

now = datetime.now()
fname = now.strftime('%Y-%m-%d') + '.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


HOST = "47.101.220.2"
PORT = 1883
topic = "/set/4GMQTT000201"

def test():
    sleeptime = 10



    client_id2 = f'python-mqtt-{random.randint(0, 1000)}'
    client2 = mqtt.Client(client_id2)
    client2.connect(HOST, PORT)
    dev2 = Device01()
    dev2.A01 = 100000
    dev2.res = '123'
    jsonstr2 = json.dumps(dev2.__dict__, default=str)
    client2.publish(topic,jsonstr2.replace(" ", ""),1)
    logging.info('关第1步 A01 100000')

    sleeptime = 5
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')




    client_id4 = f'python-mqtt-{random.randint(0, 1000)}'
    client4 = mqtt.Client(client_id4)
    client4.connect(HOST, PORT)
    dev4 = Device06()
    dev4.A06 = 100000
    dev4.res = '123'
    jsonstr4 = json.dumps(dev4.__dict__, default=str)
    client4.publish(topic,jsonstr4.replace(" ", ""),1)
    logging.info('关第2步 A06 100000 ')

    sleeptime = 5
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')



    client_id6 = f'python-mqtt-{random.randint(0, 1000)}'
    client6 = mqtt.Client(client_id6)
    client6.connect(HOST, PORT)
    dev6 = Device02()
    dev6.A02 = 100000
    dev6.res = '123'
    jsonstr6 = json.dumps(dev6.__dict__, default=str)
    client6.publish(topic,jsonstr6.replace(" ", ""),1)
    logging.info('关第3步 A02 100000 ')

    sleeptime = 5
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')




    client_id8 = f'python-mqtt-{random.randint(0, 1000)}'
    client8 = mqtt.Client(client_id8)
    client8.connect(HOST, PORT)
    dev8 = Device03()
    dev8.A03 = 100000
    dev8.res = '123'
    jsonstr8 = json.dumps(dev8.__dict__, default=str)
    client8.publish(topic,jsonstr8.replace(" ", ""),1)
    logging.info('关第4步 A03 100000 ')

    sleeptime = 5
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')



    client_id10 = f'python-mqtt-{random.randint(0, 1000)}'
    client10 = mqtt.Client(client_id10)
    client10.connect(HOST, PORT)
    dev10 = Device04()
    dev10.A04 = 100000
    dev10.res = '123'
    jsonstr10 = json.dumps(dev10.__dict__, default=str)
    client10.publish(topic,jsonstr10.replace(" ", ""),1)
    logging.info('关第5步 A04 100000 ')

    sleeptime = 5
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')

    #client.loop_forever()



if __name__ == '__main__':
    test()