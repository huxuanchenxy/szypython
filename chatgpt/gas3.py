import socket
import time
# 亲测可用
# Define the server address and port
SERVER_ADDRESS = '47.96.137.123'
SERVER_PORT = 6671

# Define the authentication message
# auth_message = 'company=shdqzdhs'
auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A'   
# auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73'   
auth_message_bytes = bytes.fromhex(auth_message)
print("auth_message_bytes:",auth_message_bytes,"END")

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Send the authentication message and receive the response
# client_socket.send(auth_message.encode())
client_socket.send(auth_message_bytes)
auth_response = client_socket.recv(1024).decode()
auth_response = auth_response.replace(' ','').replace("\n", "")
# Check if the authentication was successful
if auth_response == 'connect=ok':
    print('Authentication successful')
else:
    print('Authentication failed')

# Set the socket options to maintain the heartbeat
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 300)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 300)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

# Receive and process the data push messages
while True:
    try:
        heartbeat_message = '68 65 61 72 74 3D 6F 6B 0A'
        heartbeat_message_bytes = bytes.fromhex(heartbeat_message)
        client_socket.send(heartbeat_message_bytes)
        print("heartbeat_message_bytes",heartbeat_message_bytes,"END")
        data_push_message = client_socket.recv(1024).decode()
        print("data_push_message",data_push_message)
        # Process the data push message here
        time.sleep(60)
    except socket.error as e:
        print(e)
        print('Connection terminated')
        break