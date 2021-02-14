from socket import socket, AF_INET, SOCK_STREAM
import json
from time import sleep
import pickle

from AuditHandler import AuditHandler

server_name = 'WebService'

WEBSERVER_IP, WEBSERVER_PORT = 'web-1', 5000
TRANS_SERVER_IP, TRANS_SERVER_PORT = 'trsrvr-1', 6666
AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT = 'audit-1', 6500

web_socket = socket(AF_INET, SOCK_STREAM)
trans_socket = socket(AF_INET, SOCK_STREAM)
audit_socket = socket(AF_INET, SOCK_STREAM)
while trans_socket.connect_ex((TRANS_SERVER_IP, TRANS_SERVER_PORT)) != 0:
    sleep(1)
while audit_socket.connect_ex((AUDIT_SERVICE_IP, AUDIT_SERVICE_PORT)) != 0:
    sleep(1)


def handleCommand(data):
    print(data)
    command = data['command']
    if command == 'DUMPLOG' or command == 'DISPLAY_SUMMARY':
        resp = audit_handler.handleUserCommandEvent(
            transaction_num=data['transaction_num'],
            command=command,
            user_name=(data['user_id'] if 'user_id' in data else ''),
            filename=(data['filename'] if 'filename' in data else '')
        )
    else:
        resp = sendAndRecvObjectData(trans_socket, data)
    print(resp)


def sendAndRecvJsonData(conn, data):
    conn.sendall(json.dumps(data).encode())
    data = conn.recv(1024)
    return json.loads(data.decode())


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
    conn.sendall(json.dumps(success).encode())


def sendError(conn, status=400, reason='', content=None):
    error = {
        'status': status,
        'reason': reason,
        'content': content
    }
    conn.sendall(json.dumps(error).encode())


if __name__ == '__main__':
    global audit_handler

    audit_handler = AuditHandler(audit_socket, server_name)
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
