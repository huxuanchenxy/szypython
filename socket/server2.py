import socket


# 这个例子如果开第二个tcp客户端，第一个客户端就会close
s = socket.socket()
# host = socket.gethostname()
host = '0.0.0.0'
port = 502
s.bind((host, port))

s.listen(5)

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send(b'01 03 00 00 00 1C 44 03')
    # c.close()