import time
import paho.mqtt.client as mqtt
import json
#  from base import local_time
 
# 服务器地址
host = '47.101.220.2'
# 通信端口 默认端口1883
port = 1883

username = 'admin'
password = 'public'

# 订阅主题名
topic = '订阅主题'




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
    else:
        # 连接失败并显示错误代码
        print('Connect Error status {0}'.format(respons_code))

    # 订阅信息
    client.subscribe(topic)


# 接收到数据后事件
def on_message(client, userdata, msg):
    # 打印订阅消息主题
    print("topic", msg.topic)
    # 打印消息数据
    print("msg payload", json.loads(msg.payload))


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