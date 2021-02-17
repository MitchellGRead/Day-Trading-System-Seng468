import socket
import random

stockPort = 4444
localHost = "dummy-stock-1"


def randomNumber():
    rand = round(random.uniform(1, 400), 2)
    return rand


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((localHost, stockPort))
s.listen()

while True:
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        print(msg)
        currentTime = 42424242
        cryptoKey = '1fh5fjt'
        returnData =  f'{randomNumber()},{msg},{currentTime},{cryptoKey}'
        conn.send(returnData.encode())