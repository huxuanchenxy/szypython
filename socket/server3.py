import socket
host = '127.0.0.1'
port = 502
database = {'username': 'password'}
authmap = {}
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)
conn,addr = s.accept()
print('Got connection from', addr)
choice = conn.recv(1024).decode()
while True:
    if choice == '1':
        username = conn.recv(1024).decode()
        password = conn.recv(1024).decode()
        database.append(username)
        database.append(password)
        reply = 'Signup sucessfully'
        conn.sendall(reply.encode())
    elif choice == '2':
        user_1 = conn.recv(1024).decode()
        password_1 = conn.recv(1024).decode()
        reply = 'login failed'
        if user_1 in database:
            if password_1 == database[user_1]:
                reply = 'Login Successful'
                authmap[conn] = True
            else:
                reply = 'Wrong password'
        else:
            reply = 'Unknown user'
        conn.sendall(reply.encode())
    elif choice == '3':
        reply = 'Not Logged in, logout not necessary'
        if authmap.get(conn, False):
            del authmap[conn]
            reply = 'Logout Successfully'
        conn.sendall(reply.encode())
        break
    choice = conn.recv(1024).decode()
conn.close()