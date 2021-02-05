import socket

ip = 'localhost'
port = 5075

if __name__ == '__main__':
    webConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    webConn.bind((ip, port))
    webConn.listen(1)
    print(f'Listening on: ({ip}, {port})')

    while True:
        print('connecting...')
        conn, address = webConn.accept()
        print("connection from {}".format(address))
        while True:
            print('give me more')
            data = conn.recv(4096)
            if not data:
                break
            print(data.decode())
            conn.sendall('cause ya suck'.encode())
    print('I ended')
