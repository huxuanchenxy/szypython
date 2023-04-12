import socket
import struct
import threading
import time
from multiprocessing import JoinableQueue
 
import Message
 
 
class Client:
    def __init__(self, host, port):
        self.sock = None
        self.writer = None
        self.reader = None
        self.heartbeat_thread = None
        self.server_address = (host, port)
 
    def connect(self):
        try:
            print(f'Connecting to server{self.server_address}.')
            # 与服务端建立socket连接
            self.sock = socket.create_connection(self.server_address)
 
            # 创建并启动网络数据读取线程
            self.reader = ReaderThread(self)
            self.reader.start()
 
            # 创建并启动网络数据写入线程
            self.writer = WriterThread(self)
            self.writer.start()
 
            # 启动心跳线程
            if not self.heartbeat_thread:
                self.heartbeat_thread = HeartbeatThread(self)
                self.heartbeat_thread.start()
            print('Connected.')
        except Exception as e:
            print(f'Connection refused. {e}')
 
    def disconnect(self):
        print('Disconnected from server.')
        if self.reader:
            self.reader.dispose()
            self.reader = None
 
        if self.writer:
            self.writer.dispose()
            self.writer = None
 
        self.sock.close()
 
    # 注册连接
    def register(self):
        appid = '996da38d-a7be-4947-aa4c-f8208b5f4ade'
        imei = '869858030720693'
        self.writer.send(Message.msg_register(appid, imei))
 
    # 请求日期时间
    def request_datetime(self):
        self.writer.send(Message.msg_datetime())
 
 
# 心跳线程
class HeartbeatThread(threading.Thread):
    def __init__(self, cli):
        threading.Thread.__init__(self)
        self.cli = cli
 
    def run(self) -> None:
        while True:
            if self.cli.writer:
                self.cli.writer.send(Message.msg_heartbeat())
            else:
                self.cli.connect()
            time.sleep(3)
 
 
# 数据读取线程
class ReaderThread(threading.Thread):
    def __init__(self, cli):
        threading.Thread.__init__(self)
        self.cli = cli
        self.interrupt = False
 
    def run(self) -> None:
 
        while not self.interrupt:
            try:
                struct_bytes = self.cli.sock.recv(4)  # 数据总长度
                data_size, = struct.unpack('!I', struct_bytes)  # 解struct包
 
                data = b''  # 已接收的数据
                recv_size = 0  # 接收数据大小
                buff_size = 8192  # 接收缓冲区大小
                while recv_size < data_size:
                    remain_size = data_size - recv_size
                    if remain_size < buff_size:
                        buff_size = remain_size
                    recv_data = self.cli.sock.recv(buff_size)
                    data += recv_data
                    recv_size = len(data)
 
                if recv_size == data_size:
                    print(f'recv data: {data}, size:{len(data)}')
                    msgid, = struct.unpack('!b', data[:1])
                    error_code, = struct.unpack('!b', data[1:2])
                    print(f'msgid:{msgid}, error_code:{error_code}')
 
                    match msgid:
                        case Message.MSG_ID_DATETIME:
                            date_time = data[2:].decode('utf-8')
                            print(date_time)
 
            except Exception as e:
                print(e)
                self.cli.disconnect()
                break
 
    def dispose(self):
        self.interrupt = True
 
 
# 数据写入线程
class WriterThread(threading.Thread):
    def __init__(self, cli):
        threading.Thread.__init__(self)
        self.cli = cli
        self.interrupt = False
        self.queue = JoinableQueue(1024)
 
    def run(self) -> None:
        while not self.interrupt:
            try:
                data = self.queue.get()
                self.cli.sock.sendall(data)
            except Exception as e:
                print(e)
                self.cli.disconnect()
                break
 
    # 数据长度(4字节，不包括本身) + 数据(不定长), 大端网络字节序
    def send(self, data):
        if self.queue:
            print(f'send data: {data}, size:{len(data)}')
            data_size = struct.pack('!I', len(data))
            self.queue.put(data_size + data)
 
    def dispose(self):
        self.interrupt = True
        self.queue = None
 
 
if __name__ == '__main__':
    client = Client('127.0.0.1', 9089)
    client.connect()
    client.register()
    client.request_datetime()