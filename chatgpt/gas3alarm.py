import datetime
import decimal
import os
import socket
import sys
import time
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysqlhelperv2 import MySQLConnector
# 亲测可用


now = datetime.datetime.now()
fname = now.strftime('%Y-%m-%d') + 'gas3alarm.log'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename=fname,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )

# Define the server address and port
SERVER_ADDRESS = '47.96.137.123'
SERVER_PORT = 6671

# Define the authentication message
# auth_message = 'company=shdqzdhs'
auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A'   
# auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73'   
auth_message_bytes = bytes.fromhex(auth_message)
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(current_time,"auth_message_bytes:",auth_message_bytes,"END")
logging.info("auth_message_bytes:{}END".format(auth_message_bytes))
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Send the authentication message and receive the response
# client_socket.send(auth_message.encode())
client_socket.send(auth_message_bytes)
auth_response = client_socket.recv(1024).decode()
auth_response = auth_response.replace(' ','').replace("\n", "")
# Check if the authentication was successful
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if auth_response == 'connect=ok':
    print('Authentication successful',current_time)
    logging.info('Authentication successful')
else:
    print('Authentication failed',current_time)
    logging.info('Authentication failed')

# Set the socket options to maintain the heartbeat
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 300)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 300)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

# Receive and process the data push messages
while True:
    try:
        heartbeat_message = '68 65 61 72 74 3D 6F 6B 0A'
        heartbeat_message_bytes = bytes.fromhex(heartbeat_message)
        client_socket.send(heartbeat_message_bytes)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time,"heartbeat_message_bytes",heartbeat_message_bytes,"END")
        logprint = 'heartbeat_message_bytes:{}END'.format(heartbeat_message_bytes)
        logging.info(logprint)
        data_push_message = client_socket.recv(1024).decode()
        print(current_time,"data_push_message",data_push_message)
        logprint = 'data_push_message:{}END'.format(data_push_message)
        logging.info(logprint)
        # Process the data push message here
        str = data_push_message
        if str.find( 'imei' ) > 0:
            curdata = str[ str.find( 'imei' ): str.find( 'imei' ) + 500 ]
            imei = ''
            ccid= ''
            vers= ''
            devicetype= ''
            rssi= '' 
            snr= '' 
            count= '' 
            nh3= 0.00
            h2s= 0.00
            tvoc= '' 
            ch2o= '' 
            co2= '' 
            pm25= '' 
            pm10= '' 
            hum= '' 
            temp= '' 
            eto = 0.00
            date1= current_time
            curarr = curdata.split(';')
            for cur in curarr:
                kv = cur.split('=')
                if kv[0] == 'imei':
                    imei = kv[1]
                if kv[0] == 'ccid':
                    ccid = kv[1]
                if kv[0] == 'vers':
                    vers = kv[1]
                if kv[0] == 'type':
                    devicetype = kv[1]
                if kv[0] == 'rssi':
                    rssi = kv[1]
                if kv[0] == 'snr':
                    snr = kv[1]
                if kv[0] == 'count':
                    count = kv[1]
                if kv[0] == 'nh3':
                    nh3 = kv[1]
                if kv[0] == 'h2s':
                    h2s = kv[1]
                if kv[0] == 'tvoc':
                    tvoc = kv[1]
                if kv[0] == 'ch2o':
                    ch2o = kv[1]
                if kv[0] == 'co2':
                    co2 = kv[1]
                if kv[0] == 'pm25':
                    pm25 = kv[1]
                if kv[0] == 'pm10':
                    pm10 = kv[1]
                if kv[0] == 'hum':
                    hum = kv[1]
                if kv[0] == 'temp':
                    temp = kv[1]
                if kv[0] == 'eto':
                    eto = kv[1]
            if imei != '':
                mysql_connector = MySQLConnector('47.101.220.2', 'root', 'yfzx.2021', 'aisense')
                sql = " SELECT * FROM gas_alarm_set "
                rows = mysql_connector.execute_query(sql)

                for row in rows:
                    # print(row)
                    alarmkey = row[1]
                    limitup = row[2]
                    limitdown = row[3]
                    # alarmvalue = ""
                    flagupdown = False
                    # flagdown = False
                    if(alarmkey == "h2s"):
                        # print('h2s:',h2s)
                        alarmvalue = decimal.Decimal(h2s)
                        # print('alarmvalue:',alarmvalue)
                        # print('limitup:',limitup)
                        # print('limitdown:',limitdown)
                        if(alarmvalue > limitup):
                            flagupdown = True
                            print("h2s too high",alarmvalue,limitup)
                            logging.info("h2s too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                        if(alarmvalue < limitdown):
                            flagupdown = True
                            print("h2s too low",alarmvalue,limitdown)
                            logging.info("h2s too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
                    if(alarmkey == "nh3"):
                        # print('nh3',nh3)
                        # alarmvalue = nh3
                        alarmvalue = decimal.Decimal(nh3)
                        # print('alarmvalue',alarmvalue)
                        if(alarmvalue > limitup):
                            flagupdown = True
                            print("nh3 too high",alarmvalue,limitup)
                            logging.info("nh3 too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                        if(alarmvalue < limitdown):
                            flagupdown = True
                            print("nh3 too low",alarmvalue,limitdown)
                            logging.info("nh3 too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
                    if(alarmkey == "eto"):
                        # print('eto',eto)
                        # alarmvalue = eto
                        alarmvalue = decimal.Decimal(eto)
                        # print('alarmvalue',alarmvalue)
                        if(alarmvalue > limitup):
                            flagupdown = True
                            print("eto too high",alarmvalue,limitup)
                            logging.info("eto too high alarmvalue is{},limitup is{}".format(alarmvalue,limitup))
                        if(alarmvalue < limitdown):
                            flagupdown = True
                            print("eto too low",alarmvalue,limitdown)
                            logging.info("eto too low alarmvalue is{},limitdown is {}".format(alarmvalue,limitdown))
                    if alarmvalue != "":
                        if flagupdown == True:
                                sql1 = ("INSERT INTO `aisense`.`gas_alarm`(`imei`, `ccid`, `alarmkey`, `alarmvalue`, `limitup`, `limitdown`, `limitkey`, `status`, `date1`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                                data1 = (imei, ccid, alarmkey, alarmvalue, limitup, limitdown, alarmkey, 1, date1)
                                # id = db.insert(sql, data)
                                id = mysql_connector.execute_insert(sql1, data1)
                                print("insert sql id", id)
                                logging.info("insert sql id {}".format(id))

                imei = ''
                ccid= ''
                vers= ''
                devicetype= ''
                rssi= '' 
                snr= '' 
                count= '' 
                nh3= '' 
                h2s= '' 
                tvoc= '' 
                ch2o= '' 
                co2= '' 
                pm25= '' 
                pm10= '' 
                hum= '' 
                temp= '' 
                eto = ''
                # logging.info("insert gas sql id{}".format(ida))
                time.sleep(3)
        time.sleep(60)
    except socket.error as e:
        print(e)
        logging.error(e)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('Connection terminated',current_time)
        logging.error('Connection terminated')
        break