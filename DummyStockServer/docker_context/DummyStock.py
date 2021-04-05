import socket
import random
import config
import logging

stockPort = config.DUMMY_STOCK_SERVER_PORT
stockIp = config.DUMMY_STOCK_SERVER_IP

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if not config.RUN_DEBUG:
    logging.disable(logging.DEBUG)


def randomNumber():
    rand = round(random.uniform(1, 50), 2)
    return rand


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((stockIp, stockPort))
s.listen()

while True:
    conn, addr = s.accept()
    logger.info(f'Received connection {addr}')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        logger.info(f'Received data {msg}')
        currentTime = 42424242
        cryptoKey = '1fh5fjt'
        returnData =  f'{randomNumber()},{msg},{currentTime},{cryptoKey}'
        conn.send(returnData.encode())