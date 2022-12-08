1.要先升级pip3
python -m pip install --upgrade pip

要么pip 要么pip3

2.安装paho-mqtt
pip3 install paho.mqtt

3.安装apscheduler可以跑job 定时任务
pip3 install apscheduler

4.要读modbus
先安装:pip install modbus-tcp-server
把这个server(modbus叫slave)跑起来  modbus-tcp-server 127.0.0.1 502

5.安装 modbus_tk
pip3 install modbus_tk


