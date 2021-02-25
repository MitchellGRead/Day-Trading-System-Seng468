import socket
from time import sleep


class LegacyStockServerHandler:

    def __init__(self, ip, port, audit):
        self.ip = ip
        self.port = port
        self.audit = audit

    def quoteSocket(self):
        stockSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting Connection to Quote Server")
        while stockSocket.connect_ex((self.ip, self.port)) != 0:
            sleep(1)
        print("Quote Connection Started")
        return stockSocket

    def getQuote(self, trans_num, user_id, stock_symbol):
        stockSocket = self.quoteSocket()
        message = "{},{}\n".format(stock_symbol, user_id)
        stockSocket.send(message.encode())
        dataReceived = stockSocket.recv(1024).decode()
        dataReceived = dataReceived.split(",")
        stockSocket.close()

        result = {
            "transaction_num": trans_num,
            "user_id": user_id,
            "stock_symbol": stock_symbol,
            "price": dataReceived[0],
            "cryptokey": dataReceived[4],
            "quoteTime": dataReceived[3]
        }

        # DO AUDIT

        return dataReceived[0]
