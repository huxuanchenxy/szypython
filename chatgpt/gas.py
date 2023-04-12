import socket
import time

client = socket.socket()

ip_port = ("47.96.137.123", 6671)
client.connect(ip_port)
#client.send(b'63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A')

# a = 'company=shdqzdhs'    
# a = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A'   
a = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73'  
a_bytes = bytes.fromhex(a)
print(a_bytes)
client.send(a_bytes)

# b'\xaa\xbb\xcc\xdd\xee\xff'
data = client.recv(1024)
print(data.decode())
# while True:
#     data = client.recv(1024)
#     print(data.decode())
#     msg_input=input("please input mesage to send...")
#     client.send(msg_input.encode())
#     if msg_input== b'exit':
#         break
#     data = client.recv(1024)
#     print(data.decode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("47.96.137.123", 6671))
    while True:
        # s.sendall(b'heartbeat')
        data1 = s.recv(1024)
        print('Received1', repr(data1))

        heartbeat = '68 65 61 72 74 3D 6F 6B 0A'   
        heartbeat_bytes = bytes.fromhex(heartbeat)
        print(heartbeat_bytes)
        # client.send(heartbeat_bytes)
        s.sendall(heartbeat_bytes)
        data = s.recv(1024)
        print('Received2', repr(data))
        time.sleep(300)