# 非阻塞模块
import socketserver
import sys
import os
import time
import struct
import datetime
import binascii
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv3 import MySQLConnector
# 亲测可用


now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'server2multizhaoteng.log'
logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

my_dict = {}
#亲自测试你过，可以链接多个客户端
# 首先我们需要定义一个类
class MySocketServer(socketserver.BaseRequestHandler):
    # 首先执行setup方法，然后执行handle方法，最后执行finish方法
    # 如果handle方法报错，则会跳过
    # setup与finish无论如何都会执行
    # 一般只定义handle方法即可
    def setup(self):
        pass

    def handle(self):
        # 定义连接变量
        conn = self.request
        client_ip = ':'.join(str(x) for x in self.request.getpeername())
        # 提示信息
        print(client_ip + " 连接成功")
        logging.info('连接成功 {}'.format(client_ip))
        # 发送消息定义
        msg = "连接成功"
        # 发送消息
        #conn.send(msg.encode())
        # 进入循环 不断接收客户端消息
        while True:
            # 接收客户端消息
            data = conn.recv(1024)
            

            #data = b'\x01\x038\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x9a\xa1\xd9\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf6'
            print(' data来自ip:{}'.format(client_ip))
            logging.info('data来自ip {}'.format(client_ip))
            print(data)
            logging.info('data {}'.format(data))
            try:
                devicehex = binascii.hexlify(data).decode()
                print("devicehex {}".format(devicehex))
                logging.info('devicehex {}'.format(devicehex))
                if len(devicehex) == 30:
                    deviceid = data[4:].decode()
                    #print('deviceid:'.format(deviceid))
                    #logging.info('deviceid {}'.format(deviceid))
                    if deviceid == 'shlk2210001' or deviceid == 'shlk2210002':
                        my_dict[client_ip] = deviceid
                        print('deviceid:'.format(deviceid))
                        logging.info('deviceid {}'.format(deviceid))
                        print('my_dict[client_ip]:{}'.format(my_dict[client_ip]))
                        logging.info('my_dict[client_ip]:{}'.format(my_dict[client_ip]))

            except Exception as e:
                print(e)
                logging.info('读取deviceid报错:{}'.format(e))
                
            
            try:
                # 使用binascii.hexlify()将字节序列转换为目标形式
                hex_representation = binascii.hexlify(data).decode()
                print(hex_representation)
                logging.info('hex_representation {}'.format(hex_representation))
                print(hex_representation[94:102])
                logging.info('hex_representation 94:102 {}'.format(hex_representation[94:102]))
                byte_sequence = hex_representation[94:102]
                byte_string = bytes.fromhex(byte_sequence)
                #print(byte_string)
                # 解析为浮点数
                float_value = struct.unpack('>f', byte_string)[0]
                # 输出结果
                print("解析的浮点数:", float_value)
                logging.info('解析的浮点数:{}'.format(float_value))
                
                print("clientip:{}", client_ip)
                logging.info('clientip:{}'.format(client_ip))
                print('data my_dict[client_ip]:{}'.format(my_dict[client_ip]))
                logging.info('data my_dict[client_ip]:{}'.format(my_dict[client_ip]))
                
                
                date1 = datetime.datetime.now()
                mysql_connector1 = MySQLConnector('47.101.220.2','root', 'yfzx.2021',3306, 'aisense')
                sql1 = " INSERT INTO `aisense`.`water_zhaoteng`(`device_id`, `ec`, `cl`, `orp`, `ph`, `temp`, `tub`, `date1`) VALUES ( '{}', '-1', '-1', '-1', '-1', '-1', {}, '{}');".format(my_dict[client_ip],float_value,date1)
                mysql_connector1.execute_insert(sql1)
                print("insert waterzhaoteng sql ", sql1)
            except Exception as e:
                print(e)
                logging.info('读取data报错:{}'.format(e))
                
            
            if data == b'exit' or data == b'':
                print(client_ip + ' 连接断开')
                break

            # 打印消息
            #print(client_ip + ' send: ' + data.decode())
            heartbeat_message = '01 03 00 00 00 1C 44 03'
            heartbeat_message_bytes = bytes.fromhex(heartbeat_message)
            conn.send(heartbeat_message_bytes)
            print(' 发送到ip是:{}'.format(client_ip))
            logging.info('发送到ip是 {}'.format(client_ip))
            time.sleep(10)
        conn.close()

    def finish(self):
        pass


if __name__ == '__main__':
    # 提示信息
    print("正在等待接收数据。。。。")
    # 创建多线程实例
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 503), MySocketServer)
    # 开启异步多线程，等待连接
    server.serve_forever()