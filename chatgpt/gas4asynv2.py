import asyncio
import datetime
import socket
import time

# Define the server address and port
SERVER_ADDRESS = '47.96.137.123'
SERVER_PORT = 6671

# Define the authentication message
auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73 0A'   
# auth_message = '63 6F 6D 70 61 6E 79 3D 73 68 64 71 7A 64 68 73'   
auth_message_bytes = bytes.fromhex(auth_message)

# Define the heartbeat message
# heartbeat_message = 'heart=ok'
heartbeat_message = '68 65 61 72 74 3D 6F 6B 0A'
heartbeat_message_bytes = bytes.fromhex(heartbeat_message)

async def heartbeat():
    # Create a socket object
    client_socket = await asyncio.open_connection(SERVER_ADDRESS, SERVER_PORT)

    # Send the authentication message and receive the response
    await client_socket.send(auth_message_bytes)
    auth_response = await client_socket.read(1024)
    auth_response = auth_response.decode()
    print('auth_response',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # Check if the authentication was successful
    if auth_response == 'connect=ok':
        print('Authentication successful',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print('Authentication failed',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return

    # Set the socket options to maintain the heartbeat
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 300)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 300)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

    # Receive and process the data push messages
    last_data_push_time = time.time()
    while True:
        try:
            # client_socket.write(heartbeat_message_bytes)
            await client_socket.send(heartbeat_message_bytes)
            data_push_message = await client_socket.read(1024)
            data_push_message = data_push_message.decode()
            print("data_push_message",data_push_message,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Process the data push message here
            last_data_push_time = time.time()
        except ConnectionResetError as e:
            print('Connection terminated',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("ConnectionResetError",e)
            break
        if time.time() - last_data_push_time > 600:
            print('Connection lost for more than 10 minutes',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            break

async def main():
    await heartbeat()

asyncio.run(main())