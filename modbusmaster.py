#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: master.py
 
# ------------------------------------------------------------------------------
# 导入外部模块
# ------------------------------------------------------------------------------
 
import modbus_tk
import modbus_tk.defines
import modbus_tk.modbus
import modbus_tk.modbus_tcp
import struct
import time
 
 
 
# ------------------------------------------------------------------------------
# 主程序
# ------------------------------------------------------------------------------
 
try:
    while 1:
        master = modbus_tk.modbus_tcp.TcpMaster('127.0.0.1', 502)
	#('0.0.0.0', 502)   （master ip 地址，端口）
        #注意用linux的童鞋们，端口小于1024得用root才能跑起来哦~
	#为这个问题楼主曾经也折腾了一阵，后来才发现居然是这个原因·····
	#这里有个问题就是原来我是用'0.0.0.0'这个地址的。
	#但是它应该不能算一个ip地址了，这个是代表现有的ip地址均可的意思，有种通配符的感觉
	#在slave中可以用它，但是在master中不行，一定要给它指明一个具体的地址，看来它也有选择困难症
        master.set_timeout(3)  #timeout表示若超过3秒没有连接上slave就会自动断开
        #set_timeout(3)不知是何意----重新把timeout时间设置成3秒，在生成master那里就可以进行初始化定义的，若没有自定义就会用默认值
        aa = master.execute(1, modbus_tk.defines.READ_HOLDING_REGISTERS, 2, 10)
        #（slave id，只读，block地址，长度：即字节乘个数）
        print ("aa:" , aa, 'size', len(aa))
        bb = struct.unpack('>f', struct.pack('>HH', aa[0], aa[1]))
        #在slave中，是先打包成'>f'在以'>HH'解包的，在master中刚好相反
        #struct.unpack里解出来的是一个元组，可以用bb, = 或者输出bb[0]
        print ('bb:', bb[0])
        time.sleep(5)
except Exception as e:
    print ('=========error=========')
    print (e)
finally:
    print ('=======stop=======')