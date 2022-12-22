# ModbusTcp协议客户端模块

import socket
import random
import struct
from rich.console import Console
from rich.table import Column, Table
from rich.live import Live
from rich.panel import Panel
import time, sys
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='modbustcp.log', level=logging.DEBUG, format=LOG_FORMAT)

def connectserver(ip, port):
    try:
        mysocket = socket.socket()
        mysocket.settimeout(10)
        # mysocket.bind(("192.168.16.11",5000))
        ret = mysocket.connect((ip,port))
        if ret == socket.error:
            # print("Connect ModbusTcp server fail!")
            return None
        else:
            # print("Connect ModbusTcp server sucess!")
            return mysocket;
    except Exception as e:
        logging.debug(e)
        return None

# Modbus-RTU协议的03或04读取保存或输入寄存器功能主-》从命令帧
def modbus03or04s(add, startregadd, regnum, funcode=3):
    if add < 0 or add > 0xFF or startregadd < 0 or startregadd > 0xFFFF or regnum < 1 or regnum > 0x7D:
        print("Error: parameter error")
        return
    if funcode != 3 and funcode != 4:
        print("Error: parameter error")
        return
    # MBAP的实现
    ranvalue = random.randint(0, 0xFFFF)
    sendbytes = ranvalue.to_bytes(2, byteorder="big", signed=False)
    sendbytes = sendbytes + b"\x00\x00\x00\x06"
    sendbytes = sendbytes + add.to_bytes(1, byteorder="big", signed=False)
    # PDU实现
    sendbytes = sendbytes + funcode.to_bytes(1, byteorder="big", signed=False) + startregadd.to_bytes(2, byteorder="big", signed=False) + \
                regnum.to_bytes(2, byteorder="big", signed=False)
    # for b in list(sendbytes):
    #     print(f"{b:02x}")
    return sendbytes

# Modbus协议的03或04读取保持或输入寄存器功能从-》主的数据帧解析（浮点数2,1,4,3格式，16位短整形（定义正负数））
def modbus03or04p(recvdata, valueformat=0, intsigned=False):
    if not recvdata:
        print("Error: data error")
        return
    datalist = list(recvdata)
    if datalist[7] != 0x3 and datalist[7] != 0x4:
        print("Error: recv data funcode error")
        return
    bytenums = datalist[8]
    if bytenums % 2 != 0:
        print("Error: recv data reg data error")
        return
    retdata = []
    if valueformat == 0:
        floatnums = bytenums / 4
        # print("float nums: ", str(floatnums))
        floatlist = [0, 0, 0, 0]
        for i in range(int(floatnums)):
            floatlist[1] = datalist[9+i*4]
            floatlist[0] = datalist[10+i*4]
            floatlist[3] = datalist[11+i*4]
            floatlist[2] = datalist[12+i*4]
            bfloatdata = bytes(floatlist)
            [fvalue] = struct.unpack('f', bfloatdata)
            retdata.append(fvalue)
            # print(f'Data{i+1}: {fvalue:.3f}')
    elif valueformat == 1:
        shortintnums = bytenums / 2
        # print("short int nums: ", str(shortintnums))
        for i in range(int(shortintnums)):
            btemp = recvdata[9+i*2:11+i*2]
            shortvalue = int.from_bytes(btemp, byteorder="big", signed=intsigned)
            retdata.append(shortvalue)
            # print(f"Data{i+1}: {shortvalue}")
    return retdata    

# modbus的01或02功能号命令打包函数
def modbus01or02s(add, startregadd, regnum, funcode=2):
    if add < 0 or add > 0xFF or startregadd < 0 or startregadd > 0xFFFF or regnum < 1 or regnum > 0x7D0:
        print("Error: parameter error")
        return
    if funcode != 1 and funcode != 2:
        print("Error: parameter error")
        return
    # MBAP实现
    ranvalue = random.randint(0, 0xFFFF)
    sendbytes = ranvalue.to_bytes(2, byteorder="big", signed=False)
    sendbytes = sendbytes + b"\x00\x00\x00\x06"
    sendbytes = sendbytes + add.to_bytes(1, byteorder="big", signed=False)
    # PDU实现
    sendbytes = sendbytes + funcode.to_bytes(1, byteorder="big", signed=False) + startregadd.to_bytes(2, byteorder="big", signed=False) + \
                regnum.to_bytes(2, byteorder="big", signed=False)
    # for b in list(sendbytes):
    #     print(f"{b:02x}")
    return sendbytes

# modbus的01或02功能号的返回包解析函数
def modbus01or02p(recvdata):
    if not recvdata:
        print("Error: data error")
        return
    datalist = list(recvdata)
    if datalist[7] != 0x1 and datalist[7] != 0x2:
        print("Error: recv data funcode error")
        return
    bytenums = datalist[8]
    ret_data = []
    for i in range(bytenums):
        intvalue = int(recvdata[9+i])
        for bit in range(8):
            nowvalue = intvalue & 0x01
            intvalue = intvalue >> 1
            ret_data.append(nowvalue)
    return ret_data

# 读取仪表数据并解析返回
def readmeterdata(mysocket, meter_add, start_reg, reg_num):
    try:
        send_data = modbus03or04s(meter_add, start_reg, reg_num)
        if not send_data:
            print("读取命令处理错误！")
            return
        starttime = time.time()
        mysocket.send(send_data)
        recv_data = mysocket.recv(1024) #(reg_num*2+9)
        endtime = time.time()
        # print(f"Used time is {endtime-starttime:.3f}")
        if recv_data and len(recv_data) > 0:
            retdata = modbus03or04p(recv_data)
            if retdata:
                return retdata
            else:
                return
        else:
            return
    except Exception as e:
        # print(f"Exception : {e}")
        endtime = time.time()
        print(f"读取超时时间: {endtime-starttime:.3f}")        
        return

# 读取仪表数据并解析返回
def readmeterdata2(mysocket, meter_add, start_reg, reg_num):
    try:
        send_data = modbus01or02s(meter_add, start_reg, reg_num)
        if not send_data:
            print("读取命令处理错误！")
            return
        starttime = time.time()
        mysocket.send(send_data)
        recv_data = mysocket.recv(1024) #(reg_num*2+9)
        endtime = time.time()
        # print(f"Used time is {endtime-starttime:.3f}")
        if recv_data and len(recv_data) > 0:
            retdata = modbus01or02p(recv_data)
            if retdata:
                return retdata
            else:
                return
        else:
            return
    except Exception as e:
        # print(f"Exception : {e}")
        endtime = time.time()
        print(f"读取超时时间: {endtime-starttime:.3f}")        
        return   


def generate_table(regdata, nowdata) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("No", width = 4)
    table.add_column('RegAdd', width=12)
    table.add_column("Data", width=12)
    for i in range(len(nowdata)):
        table.add_row("[red]"+str(i + 1), f"[yellow]{regdata[i]}", f"[green]{nowdata[i]:.3f}")
    return table        

if __name__ == "__main__":

    funcode = 2
    slaveadd = 2
    startreg = 1
    regnums = 15
    serverip = "192.168.16.253"
    serverport = 502
    regStartName = 40001
    logging.debug("Modbus/Tcp Start!")
    funcode = int(input("Modbus功能号(01或02或03或04)："))
    slaveadd = int(input("Modbus从站地址："))
    startreg = int(input("开始寄存器地址："))
    regnums = int(input("寄存器个数："))

    # 连接MODBUSTCP服务器
    mysocket = connectserver(serverip, serverport)
    if not mysocket:
        print("Connect MoudbusTcp Server Fail!")
    else:
        # 读取寄存器数据值，用rich模块的表格实时显示数据，没有数据则模拟随机数据
        if funcode == 3 or funcode == 4 :
            if funcode == 3:
                regStartName = 40001
            else:
                regStartName = 30001
            now_data = readmeterdata(mysocket, slaveadd, startreg, regnums)
            if not now_data:
                now_data = []
                for i in range(int(regnums/2)):
                    value = random.random() * 100
                    now_data.append(value)
            readnums = 10
            errnums = 0
            regdata = [ regStartName+startreg+reg*2 for reg in range(int(regnums/2)) ]
            with Live(generate_table(regdata, now_data), refresh_per_second=4) as live:
                for _ in range(readnums):
                    time.sleep(0.4)
                    now_data = readmeterdata(mysocket, slaveadd, startreg, regnums)
                    if not now_data:
                        now_data = []
                        for i in range(int(regnums / 2)):
                            value = random.random() * 100
                            now_data.append(value)
                        errnums += 1
                    live.update(generate_table(regdata, now_data))
            # print(f"\nread nums={readnums},  err nums={errnums}")
            console = Console()
            strmsg = f"读取次数={readnums}, 错误次数={errnums}"
            console.print(Panel("[yellow]" + strmsg, title="通信统计"))

        if funcode == 1 or funcode == 2 :
            if funcode == 1:
                regStartName = 0
            else:
                regStartName = 10000
            now_data = readmeterdata2(mysocket, slaveadd, startreg, regnums)
            if not now_data:
                for x in range(regnums):
                    now_data.append(0)
            else:
                if len(now_data) > regnums:
                    now_data = now_data[:regnums]            
            readnums = 15
            errnums = 0
            regdata = [ regStartName+startreg+reg for reg in range(int(regnums)) ]
            with Live(generate_table(regdata, now_data), refresh_per_second=4) as live:
                for _ in range(readnums):
                    time.sleep(0.4)
                    now_data = readmeterdata2(mysocket, slaveadd, startreg, regnums)
                    if not now_data:
                        errnums += 1
                        for x in range(regnums):
                            now_data.append(0)
                    else:
                        if len(now_data) > regnums:
                            now_data = now_data[:regnums]
                    live.update(generate_table(regdata, now_data))
            console = Console()
            strmsg = f"读取次数={readnums}, 错误次数={errnums}"
            console.print(Panel("[yellow]" + strmsg, title="通信统计"))
        mysocket.close()
