import time
import socket
import Message
import threading
from struct import unpack
 
 
# 字节转字符串
def bytes2str(bytes):
    return bytes.decode('utf-8')
 
 
class Server:
    def __init__(self):
        # 服务器ip与端口
        self.server_address = ('127.0.0.1', 9089)
 
    def start(self):
        # 监听端口
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(self.server_address)
            sock.listen(1024)
            print(f'Server started on {self.server_address}')
 
            while True:
                try:
                    client_socket, addr = sock.accept()
                    handler = RequestHandler(client_socket, addr)
                    thread = threading.Thread(target=handler.run, args=())
                    thread.start()
                except Exception as ex:
                    print(ex)
 
 
class RequestHandler:
    def __init__(self, sock, client_address):
        self.sock = sock
        self.client_address = client_address
 
    def run(self):
        try:
            while True:
                struct_bytes = self.sock.recv(4)  # 读取数据长度(4字节)
                data_size, = unpack('!I', struct_bytes)  # 解struct包，转换为数据长度
 
                data = b''  # 已接收的数据
                recv_size = 0  # 接收数据大小
                buff_size = 8192  # 接收缓冲区大小
                while recv_size < data_size:
                    remain_size = data_size - recv_size  # 计算剩余数据长度
                    if remain_size < buff_size:  # 如果剩余数据长度小于缓冲区长度时，设置缓冲区长度为剩余数据长度
                        buff_size = remain_size
                    recv_data = self.sock.recv(buff_size)  # 接收数据
                    data += recv_data  # 数据累加
                    recv_size = len(data)  # 计算已接收的数据长度
 
                if recv_size == data_size:  # 当数据接收完成时，对数据进行解析和处理
                    print(f'recv data from {self.client_address}, data_size:', len(data))
                    msgid, = unpack('!b', data[:1])  # 读取消息ID，根据消息ID区分处理
                    match msgid:
                        case Message.MSG_ID_REGISTER:
                            appid = bytes2str(data[1:37])
                            imei = bytes2str(data[37:52])
                            print(f'appid: {appid}, imei: {imei}')
                            error_code = 0  # 错误码 0正常 -1错误
                            response = Message.pack('!I2b', 2, msgid, error_code)
                            self.sock.sendall(response)
                        case Message.MSG_ID_HEARTBEAT:
                            error_code = 0  # 错误码 0正常 -1错误
                            response = Message.pack('!I2b', 2, msgid, error_code)
                            self.sock.sendall(response)
                        case Message.MSG_ID_DATETIME:
                            strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            str_len = len(strtime)
                            error_code = 0  # 错误码 0正常 -1错误
                            response = Message.pack(f'!I2b{str_len}s', 2 + str_len, msgid, error_code, strtime)
                            self.sock.sendall(response)
 
        except Exception as ex:
            print(f"{ex} {self.client_address}")
 
 
if __name__ == '__main__':
    Server().start()