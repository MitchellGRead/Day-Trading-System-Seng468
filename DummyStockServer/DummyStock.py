import socket
import random
import json

stockPort = 4444
localHost = "localhost"


def randomNumber():
    rand = round(random.uniform(1, 400), 2)
    return rand


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((localHost, stockPort))
s.listen()
conn, addr = s.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
    msg = data.decode()
    print(msg)
    returnData = str(randomNumber()) + ", " + msg + ", 1k2j3h4g5f6"
    conn.send(returnData.encode())
