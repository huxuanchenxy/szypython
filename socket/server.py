import socket
import struct


def server_program():
    # get the hostname
    # host = socket.gethostname()
    # print(host)
    host = "0.0.0.0"
    port = 502  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024)
        
        #data = conn.recv(1024).decode()
        # print('1:')
        # print(data)
        # print('11111:')
        # fff = struct.unpack('!f',data)[0]
        # print(fff)
        # print('2:')
        # print(data.decode('utf-8','ignore'))
        # print('3:')
        # temp1 = bytes.fromhex(data.decode('utf-8','ignore'))
        # print(temp1)
        # print('4:')
        # temp2 = temp1.hex()
        # print(temp2)
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        #f1 = struct.unpack('!f',bytes.fromhex(data.decode('utf-8','ignore')))[0]
        f1 = struct.unpack('!f',data)[0]
        print(f1)
        # data = input(' -> ')
        #  conn.send(data.encode())  # send data to the client
        conn.send(data)
    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()