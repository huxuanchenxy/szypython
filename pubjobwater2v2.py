# encoding: utf-8
import random
import time
# from datetime import datetime
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import json
from apscheduler.schedulers.background  import BlockingScheduler
import logging
from apscheduler.triggers.cron import CronTrigger
import schedule

class Device01:
    A01 = 110000
    res = '123'

class Device02:
    A02 = 110000
    res = '123'


now = datetime.now()
fname = now.strftime('%Y-%m-%d') + 'pubjobwater2V2.log'

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
topic = "/set/INDOOR00012799" #室内机
topic2 = "/set/OUTDOOR00012798" #室外机


def test2():
    for i in range(3):
        logging.info('循环第 {} 次'.format(i))
        sleeptime = 10
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        client = mqtt.Client(client_id)
        client.connect(HOST, PORT)
        dev1 = Device02()
        dev1.A02 = 110000
        dev1.res = 'OUTDOOR00012798'
        jsonstr = json.dumps(dev1.__dict__, default=str)
        client.publish(topic2,jsonstr.replace(" ", ""),1)
        logging.info('室外机2 开 110000')

        sleeptime = 50
        time.sleep(sleeptime)
        logging.info('sleep '+ str(sleeptime) +' 秒')

        client_id1 = f'python-mqtt-{random.randint(0, 1000)}'
        client1 = mqtt.Client(client_id1)
        client1.connect(HOST, PORT)
        dev1 = Device02()
        dev1.A02 = 100000
        dev1.res = 'OUTDOOR00012798'
        jsonstr = json.dumps(dev1.__dict__, default=str)
        client1.publish(topic2,jsonstr.replace(" ", ""),1)
        logging.info('室外机2 关 100000')

        sleeptime = 10
        time.sleep(sleeptime)
        logging.info('sleep '+ str(sleeptime) +' 秒')
    #client.loop_forever()

# def dojob():
#     #创建调度器：BlockingScheduler
#     scheduler = BlockingScheduler()
#     #添加任务,时间间隔2S
#     # scheduler.add_job(test, 'interval', hours=2)
#     scheduler.add_job(test2, 'interval', minutes=27)
#     #scheduler.add_job(test, 'interval', hours=2)
#     #scheduler.add_job(test, CronTrigger.from_crontab('0 0/2 * * *'))
#     #scheduler.add_job(test, 'cron', day_of_week='*', hour='*', minute='2',start_date='2012-10-10 09:30:00')
#     scheduler.start()

# if __name__ == '__main__':
#     test2()
#     dojob()

def schedule_job_at_specific_time(start_time):
    now = datetime.now().time()
    if now < start_time:
        delay = (datetime.combine(datetime.today(), start_time) - datetime.now()).seconds
    else:
        delay = (datetime.combine(datetime.today(), start_time) + timedelta(days=1) - datetime.now()).seconds
    time.sleep(delay)
    test2()

start_time = datetime.strptime("13:17", "%H:%M").time()
schedule_job_at_specific_time(start_time)
# schedule.every(30).minutes.at("11:16").do(test2)
schedule.every(27).minutes.do(test2)

while True:
    schedule.run_pending()
    # time.sleep(1)