#!/usr/bin/python3
import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import time
import datetime
import struct

# 读模拟量 https://blog.csdn.net/lzl640/article/details/118722675
def read_AI():
    AI = {}
    master_0 = mt.TcpMaster(
        "127.0.0.1",
        502
    )
    master_0.set_timeout(10.0)
    try:
        a_0 = master_0.execute(1, md.READ_HOLDING_REGISTERS, 0, 100)      
        print(a_0)
        AI[0] =float('%.2f' % int2float(a_0[0], a_0[1]))# 锅炉蒸发量
        AI[1] =float(a_0[2]/100.0)# 转速        
    except BaseException as e:
        print(e)
    return (AI)

# 读开关量
def read_DI():
    DI = {}
    master_0 = mt.TcpMaster(
        "127.0.0.1",
        503
    )
    master_0.set_timeout(5.0)
    try:
        d_0 = master_0.execute(1, md.READ_DISCRETE_INPUTS, 3072, 4)        
        DI[0] = d_0[0]# 运行
        DI[1] = d_0[1]# 停运
        DI[2] = d_0[2]# 阀门开
        DI[3] = d_0[3]# 阀门关
    except BaseException as e:
        print(e)
    return (DI)

# 浮点数转换
def int2float(a,b):
    f=0
    try:
        z0=hex(a)[2:].zfill(4) #取0x后边的部分
        z1=hex(b)[2:].zfill(4) #取0x后边的部分
        z=z1+z0 #高字节在前 低字节在后
        f=struct.unpack('!f', bytes.fromhex(z))[0] #返回浮点数
        #z=z0+z1 #低字节在前 高字节在后
        #print (z)
    except BaseException as e:
        print(e)     
    return f

# 自我测试
if __name__ == "__main__":
    print(read_AI())
    #print(read_DI())
