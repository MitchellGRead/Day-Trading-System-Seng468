import socket
import random
import config

stockPort = config.DUMMY_STOCK_SERVER_PORT
stockIp = config.DUMMY_STOCK_SERVER_IP


def randomNumber():
    rand = round(random.uniform(1, 50), 2)
    return rand


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((stockIp, stockPort))
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