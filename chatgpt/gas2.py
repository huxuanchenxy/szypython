import socket
import time


# Define the server address and port
SERVER_ADDRESS = '47.96.137.123'
SERVER_PORT = 6671

# Define the authentication message
auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A'   
# auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73'   
auth_message_bytes = bytes.fromhex(auth_message)
print("11",auth_message_bytes,"22")
# client.send(a_bytes)
# auth_message = 'company=shdqzdhs'

# Define the heartbeat message
# heartbeat_message = 'heart=ok'
heartbeat_message = '68 65 61 72 74 3D 6F 6B 0A'
heartbeat_message_bytes = bytes.fromhex(heartbeat_message)
print("11",heartbeat_message_bytes,"22")

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

# Send the authentication message and receive the response
# client_socket.send(auth_message.encode())
client_socket.sendall(auth_message_bytes)
auth_response = client_socket.recv(1024).decode()
# print("11",auth_response+"22")
flag = auth_response.replace(' ','').replace("\n", "") == "connect=ok"
# print(flag)
# Check if the authentication was successful
# if auth_response == "connect=ok":
if flag:
    print('Authentication successful')
else:
    print('Authentication failed')

# Send the heartbeat message every 10 seconds
while True:
    try:
        # client_socket.send(heartbeat_message.encode())
        client_socket.send(heartbeat_message_bytes)
        heartbeat_response = client_socket.recv(1024).decode()
        print("11",heartbeat_response,"22")
        if heartbeat_response.replace(' ','').replace("\n", "") != 'heart=ok':
            print('Heartbeat failed')
            break
        time.sleep(300)
    except socket.error:
        print('Connection terminated')
        break

# Receive and process the data push messages
while True:
    try:
        data_push_message = client_socket.recv(1024).decode()
        print("data_push_message:",data_push_message)
        # Process the data push message here
        time.sleep(300)
    except socket.error as e:
        print(e)
        print('Connection terminated')
        break