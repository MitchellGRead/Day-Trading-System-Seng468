from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from audit import EventTypes
import pickle

WEBSERVER_IP, WEBSERVER_PORT = 'localhost', 5000
TRANS_SERVER_IP, TRANS_SERVER_PORT = 'localhost', 6666
AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT = 'localhost', 6500

web_socket = socket(AF_INET, SOCK_STREAM)
trans_socket = socket(AF_INET, SOCK_STREAM)
audit_socket = socket(AF_INET, SOCK_STREAM)
while trans_socket.connect_ex((TRANS_SERVER_IP, TRANS_SERVER_PORT)) != 0:
    sleep(1)
while audit_socket.connect_ex((AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT)) != 0:
    sleep(1)


def handleCommand(data):
    print(data)
    resp = sendAndRecvJsonData(trans_socket, data)
    # Log operation
    print(resp)


def sendAndRecvJsonData(conn, data):
    conn.sendall(pickle.dumps(data))
    data = conn.recv(1024)
    return pickle.loads(data)


def sendAndRecvObjectData(conn, data):
    conn.sendall(pickle.dumps(data))
    data = conn.recv(4096)
    return pickle.loads(data)


def checkRequest(data):
    return 'command' in data and 'user_id' in data


def sendSuccess(conn, status=200):
    success = {
        'status': status
    }
    conn.sendall(pickle.dumps(success))


def sendError(conn, status=400, reason='', content=None):
    error = {
        'status': status,
        'reason': reason,
        'content': content
    }
    conn.sendall(pickle.dumps(error))


if __name__ == '__main__':
    web_socket.bind((WEBSERVER_IP, WEBSERVER_PORT))
    web_socket.listen(5)
    while True:
        print(f'Listening on ({WEBSERVER_IP}, {WEBSERVER_PORT})')
        conn, address = web_socket.accept()
        print(f'Connection from {address}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = pickle.loads(data)

            if True:
                # checkRequest(data):
                handleCommand(data)
                sendSuccess(conn)
            else:
                sendError(conn, reason='Invalid request. Requires command and user_id.', content=data)
