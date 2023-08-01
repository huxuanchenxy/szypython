import socket

def send_login_message(client_socket):
    # 发送登录报文
    login_message = "Login message"
    client_socket.send(login_message.encode())

def send_custom_message(client_socket):
    # 发送自定义报文
    custom_message = "Custom message"
    client_socket.send(custom_message.encode())

def receive_heartbeat_message(client_socket):
    # 接收心跳报文
    heartbeat_message = client_socket.recv(1024).decode()
    # 处理心跳报文
    # ...

def main():
    # 服务器的IP和端口
    server_ip = "127.0.0.1"
    server_port = 503

    # 创建客户端socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接服务器
        client_socket.connect((server_ip, server_port))
        print("Connected to server")

        # 发送登录报文
        send_login_message(client_socket)

        while True:
            # 接收心跳报文
            receive_heartbeat_message(client_socket)

            # 发送自定义报文
            send_custom_message(client_socket)

    except Exception as e:
        print("Error:", e)

    finally:
        # 关闭客户端socket
        client_socket.close()

if __name__ == "__main__":
    main()