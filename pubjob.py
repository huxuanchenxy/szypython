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
    time = datetime.now()
    res = '123'

class Device02:
    A02 = 110000
    time = datetime.now()
    res = '123'

class Device03:
    A03 = 110000
    time = datetime.now()
    res = '123'

class Device04:
    A04 = 110000
    time = datetime.now()
    res = '123'

class Device06:
    A06 = 110000
    time = datetime.now()
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
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(client_id)
    client.connect(HOST, PORT)
    dev1 = Device01()
    dev1.A01 = 110000
    dev1.time = datetime.now()
    dev1.res = '123'
    jsonstr = json.dumps(dev1.__dict__, default=str)
    client.publish(topic,jsonstr,1)
    logging.info('第1步 A01 110000')

    sleeptime = 10
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id2 = f'python-mqtt-{random.randint(0, 1000)}'
    client2 = mqtt.Client(client_id2)
    client2.connect(HOST, PORT)
    dev2 = Device01()
    dev2.A01 = 100000
    dev2.time = datetime.now()
    dev2.res = '123'
    jsonstr2 = json.dumps(dev2.__dict__, default=str)
    client2.publish(topic,jsonstr2,1)
    logging.info('第2步 A01 100000')

    sleeptime = 1
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id3 = f'python-mqtt-{random.randint(0, 1000)}'
    client3 = mqtt.Client(client_id3)
    client3.connect(HOST, PORT)
    dev3 = Device06()
    dev3.A06 = 110000
    dev3.time = datetime.now()
    dev3.res = '123'
    jsonstr3 = json.dumps(dev3.__dict__, default=str)
    client3.publish(topic,jsonstr3,1)
    logging.info('第3步 A06 110000')

    sleeptime = 10
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id4 = f'python-mqtt-{random.randint(0, 1000)}'
    client4 = mqtt.Client(client_id4)
    client4.connect(HOST, PORT)
    dev4 = Device06()
    dev4.A06 = 100000
    dev4.time = datetime.now()
    dev4.res = '123'
    jsonstr4 = json.dumps(dev4.__dict__, default=str)
    client4.publish(topic,jsonstr4,1)
    logging.info('第4步 A06 100000 ')

    sleeptime = 1
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id5 = f'python-mqtt-{random.randint(0, 1000)}'
    client5 = mqtt.Client(client_id5)
    client5.connect(HOST, PORT)
    dev5 = Device02()
    dev5.A02 = 110000
    dev5.time = datetime.now()
    dev5.res = '123'
    jsonstr5 = json.dumps(dev5.__dict__, default=str)
    client5.publish(topic,jsonstr5,1)
    logging.info('第5步 A02 110000 ')

    sleeptime = 10
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id6 = f'python-mqtt-{random.randint(0, 1000)}'
    client6 = mqtt.Client(client_id6)
    client6.connect(HOST, PORT)
    dev6 = Device02()
    dev6.A02 = 100000
    dev6.time = datetime.now()
    dev6.res = '123'
    jsonstr6 = json.dumps(dev6.__dict__, default=str)
    client6.publish(topic,jsonstr6,1)
    logging.info('第6步 A02 100000 ')

    sleeptime = 1
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id7 = f'python-mqtt-{random.randint(0, 1000)}'
    client7 = mqtt.Client(client_id7)
    client7.connect(HOST, PORT)
    dev7 = Device03()
    dev7.A03 = 110000
    dev7.time = datetime.now()
    dev7.res = '123'
    jsonstr7 = json.dumps(dev7.__dict__, default=str)
    client7.publish(topic,jsonstr7,1)
    logging.info('第7步 A03 110000 ')

    sleeptime = 10
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id8 = f'python-mqtt-{random.randint(0, 1000)}'
    client8 = mqtt.Client(client_id8)
    client8.connect(HOST, PORT)
    dev8 = Device03()
    dev8.A03 = 100000
    dev8.time = datetime.now()
    dev8.res = '123'
    jsonstr8 = json.dumps(dev8.__dict__, default=str)
    client8.publish(topic,jsonstr8,1)
    logging.info('第8步 A03 100000 ')

    sleeptime = 1
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')



    client_id9 = f'python-mqtt-{random.randint(0, 1000)}'
    client9 = mqtt.Client(client_id9)
    client9.connect(HOST, PORT)
    dev9 = Device04()
    dev9.A04 = 110000
    dev9.time = datetime.now()
    dev9.res = '123'
    jsonstr9 = json.dumps(dev9.__dict__, default=str)
    client9.publish(topic,jsonstr9,1)
    logging.info('第9步 A04 110000 ')

    sleeptime = 10
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')


    client_id10 = f'python-mqtt-{random.randint(0, 1000)}'
    client10 = mqtt.Client(client_id10)
    client10.connect(HOST, PORT)
    dev10 = Device04()
    dev10.A04 = 100000
    dev10.time = datetime.now()
    dev10.res = '123'
    jsonstr10 = json.dumps(dev10.__dict__, default=str)
    client10.publish(topic,jsonstr10,1)
    logging.info('第10步 A04 100000 ')

    sleeptime = 1
    time.sleep(sleeptime)
    logging.info('sleep '+ str(sleeptime) +' 秒')

    #client.loop_forever()

def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    scheduler.add_job(test, 'interval', minutes=5)
    #scheduler.add_job(test, 'interval', hours=2)
    #scheduler.add_job(test, CronTrigger.from_crontab('0 0/2 * * *'))
    #scheduler.add_job(test, 'cron', day_of_week='*', hour='*', minute='2',start_date='2012-10-10 09:30:00')
    scheduler.start()

if __name__ == '__main__':
    test()
    dojob()