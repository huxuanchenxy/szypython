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
flag = 1

my_dict = {}

while True:
    data = b'\x01\x038\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x9a\xa1\xd9\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xf6'
    client_ip1 = "112.3.57.116:15625"
    client_ip2 = "112.3.57.116:44444"
    client_ip = ''
    # print(' data来自ip:{}'.format(client_ip))
    # logging.info('data来自ip {}'.format(client_ip))
    print(data)
    logging.info('data {}'.format(data))
    try:
        # d1 = b'\xff\r\t\x01shlk2210002'
        # devicehex = binascii.hexlify(d1).decode()
        # devicehex =  b'ff0d090173686c6b32323130303032'
        # print('devicehex:{}'.format(devicehex))
        # hex_string = 'ff0d090173686c6b32323130303032'
        # byte_string = bytes.fromhex(hex_string)
        # length = len(byte_string)
        # print('length:{}'.format(length))
        # if len(devicehex) == 30:
        # if length == 15:
        #     deviceid = data[4:].decode()
        #     #print('deviceid:'.format(deviceid))
        #     #logging.info('deviceid {}'.format(deviceid))
        #     if deviceid == 'shlk2210001' or deviceid == 'shlk2210002':
        # print('deviceid:{}'.format(deviceid))
        # logging.info('deviceid {}'.format(deviceid))
        deviceid1 = 'shlk2210001'
        deviceid2 = 'shlk2210002'
        if flag == 1:
            client_ip = client_ip1
            my_dict[client_ip] = deviceid1
        if flag == 2:
            client_ip = client_ip2
            my_dict[client_ip] = deviceid2

        flag = flag + 1
        if flag > 2:
            flag = 1

    except Exception as e:
        print(e)
        logging.info('读取deviceid报错:{}'.format(e))
        

    try:
        # 使用binascii.hexlify()将字节序列转换为目标形式
        hex_representation = binascii.hexlify(data).decode()
        print("hex_representation {}".format(hex_representation))
        logging.info('hex_representation {}'.format(hex_representation))
        print("hex_representation 86:94:{}".format(hex_representation[86:94]))
        logging.info('hex_representation 86:94: {}'.format(hex_representation[86:94]))
        byte_sequence = hex_representation[86:94]
        byte_string = bytes.fromhex(byte_sequence)
        #print(byte_string)
        # 解析为浮点数
        float_value = struct.unpack('>f', byte_string)[0]
        # 输出结果
        print("解析的浮点数:{}", float_value)
        logging.info('解析的浮点数:{}'.format(float_value))

        print("clientip:{}", client_ip)
        print("my_dict[client_ip]:{}", my_dict[client_ip])
        date1 = datetime.datetime.now()
        mysql_connector1 = MySQLConnector('47.101.220.2','root', 'yfzx.2021',3306, 'aisense')
        sql1 = " INSERT INTO `aisense`.`water_zhaotengtest`(`device_id`, `ec`, `cl`, `orp`, `ph`, `temp`, `tub`, `date1`) VALUES ( '{}', '-1', '-1', '-1', '-1', '-1', {}, '{}');".format(my_dict[client_ip],float_value,date1)
        mysql_connector1.execute_insert(sql1)
        print("insert waterzhaoteng sql ", sql1)

    except Exception as e:
        print(e)
        logging.info('读取data报错:{}'.format(e))

    time.sleep(10)


