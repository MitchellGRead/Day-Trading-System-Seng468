from socket import socket, AF_INET, SOCK_STREAM
import json


WEBSERVER_IP, WEBSERVER_PORT = 'localhost', 5000
web_socket = socket(AF_INET, SOCK_STREAM)


def handleCommand(data):
    command = data['command']
    if command == 'ADD':
        print('add')


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

            if checkRequest(data):
                handleCommand(data)
                sendSuccess(conn)
            else:
                sendError(conn, reason='Invalid request. Requires command and user_id.', content=data)


