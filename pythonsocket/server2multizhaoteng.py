# 非阻塞模块
import socketserver

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
        # 发送消息定义
        msg = "连接成功"
        # 发送消息
        conn.send(msg.encode())
        # 进入循环 不断接收客户端消息
        while True:
            # 接收客户端消息
            data = conn.recv(1024)

            # 输出shlk2210001
            # hex_string = "73 68 6C 6B 32 32 31 30 30 30 31"
            # ascii_string = bytearray.fromhex(hex_string).decode('utf-8')
            # print(ascii_string)
            # 输出shlk2210001


            # 输出0.05849429202055931
            # import struct

            # hex_string = "3D 6F 97 C1"
            # byte_array = bytearray.fromhex(hex_string)
            # byte_array.reverse()  # 将字节数组反转

            # reg1 = byte_array[:2]  # 取前两个字节作为第一个寄存器
            # reg2 = byte_array[2:]  # 取后两个字节作为第二个寄存器

            # float_value1 = struct.unpack('!f', reg1)[0]
            # float_value2 = struct.unpack('!f', reg2)[0]

            # print(float_value1 + float_value2)
            # 输出0.05849429202055931


            if data == b'exit' or data == b'':
                print(client_ip + ' 连接断开')
                break

            # 打印消息
            print(client_ip + ' send: ' + data.decode())
            conn.send(data)
        conn.close()

    def finish(self):
        pass


if __name__ == '__main__':
    # 提示信息
    print("正在等待接收数据。。。。")
    # 创建多线程实例
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 502), MySocketServer)
    # 开启异步多线程，等待连接
    server.serve_forever()