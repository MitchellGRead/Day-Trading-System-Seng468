from socket import socket, AF_INET, SOCK_STREAM
import json
from time import sleep

WEBSERVER_IP, WEBSERVER_PORT = 'localhost', 5000
TRANS_SERVER_IP, TRANS_SERVER_PORT = 'localhost', 6666

web_socket = socket(AF_INET, SOCK_STREAM)
trans_socket = socket(AF_INET, SOCK_STREAM)
while trans_socket.connect_ex((TRANS_SERVER_IP, TRANS_SERVER_PORT)) != 0:
    sleep(1)


def handleCommand(data):
    print(data)
    resp = sendAndRecvData(trans_socket, data)
    # Log operation
    print(resp)


def sendAndRecvData(conn, data):
    conn.sendall(json.dumps(data).encode())
    data = conn.recv(1024)
    return json.loads(data.decode())


def checkRequest(data):
    return 'command' in data and 'user_id' in data


def sendSuccess(conn, status=200):
    success = {
        'status': status
    }
    conn.sendall(json.dumps(success).encode())


def sendError(conn, status=400, reason='', content=None):
    error = {
        'status': status,
        'reason': reason,
        'content': content
    }
    conn.sendall(json.dumps(error).encode())


if __name__ == '__main__':
    web_socket.bind((WEBSERVER_IP, WEBSERVER_PORT))
    web_socket.listen(5)
    while True:
        print(f'Listening on ({WEBSERVER_IP}, {WEBSERVER_PORT})')
        conn, address = web_socket.accept()
        print(f'Connection from {address}')
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            data = json.loads(data)

            if True: #checkRequest(data):
                handleCommand(data)
                sendSuccess(conn)
            else:
                sendError(conn, reason='Invalid request. Requires command and user_id.', content=data)
