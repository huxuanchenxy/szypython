import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import logging
#  from base import local_time
 
# 服务器地址
host = '47.101.220.2'
# 通信端口 默认端口1883
port = 1883

username = 'admin'
password = 'public'

# 订阅主题名
topic = '/water/guozhan'

now = datetime.now()
fname = now.strftime('%Y-%m-%d') + 'sub_water_guozhan.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )


def local_time():
    times = time.time()
    local_time = time.localtime(times)
    print("运行时间戳：", time.strftime("%Y-%m-%d %H:%M:%S", local_time))

# 连接后事件
def on_connect(client, userdata, flags, respons_code):
    local_time()

    if respons_code == 0:
        # 连接成功
        print('Connection Succeed!')
        logging.info('Connection Succeed!')
    else:
        # 连接失败并显示错误代码
        print('Connect Error status {0}'.format(respons_code))
        logging.info('Connect Error status {0}'.format(respons_code))
    # 订阅信息
    client.subscribe(topic)


# 接收到数据后事件
def on_message(client, userdata, msg):
    # 打印订阅消息主题
    print("topic", msg.topic)
    # 打印消息数据
    print("msg payload", json.loads(msg.payload))
    logging.info(json.loads(msg.payload))

def main_demo():
    client = mqtt.Client()

    # 注册事件
    client.on_connect = on_connect
    client.on_message = on_message

    # 设置账号密码（如果需要的话）
    client.username_pw_set(username, password=password)

    # 连接到服务器
    client.connect(host, port=port, keepalive=60)

    # 守护连接状态
    client.loop_forever()



if __name__ == '__main__':
    main_demo()