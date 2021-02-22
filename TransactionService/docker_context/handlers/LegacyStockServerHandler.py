import socket
from time import sleep
from datetime import datetime
import pickle


class LegacyStockServerHandler:

    def __init__(self, ip, port, redis, audit):
        self.ip = ip
        self.port = port
        self.redis = redis
        self.audit = audit

    def quoteSocket(self):
        stockSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting Connection to Quote Server")
        while stockSocket.connect_ex((self.ip, self.port)) != 0:
            sleep(1)
        print("Quote Connection Started")
        return stockSocket

    def getQuote(self, trans_num, user_id, stock_symbol):
        if self.redis.exists("quotes"):
            quotes = self.redis.get("quotes")
            quotes = pickle.loads(quotes)
            then = quotes[1]
            now = datetime.now()
            elapsedTime = now - then
            duration = elapsedTime.total_seconds()
            if duration < 60:
                return quotes[0]
        else:
            stockSocket = self.quoteSocket()
            message = "{},{}\n".format(stock_symbol, user_id)
            stockSocket.send(message.encode())
            dataReceived = stockSocket.recv(1024).decode()
            dataReceived = dataReceived.split(",")
            if self.redis.exists("quotes"):
                quotes = self.redis.get("quotes")
                quotes = pickle.loads(quotes)
                quotes[stock_symbol] = [dataReceived[0], datetime.now()]
                self.redis.set("quotes", pickle.dumps(quotes))
            else:
                quotes = {stock_symbol: [dataReceived[0], datetime.now()]}
                self.redis.set("quotes", pickle.dumps(quotes))
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
            # FINALIZE RETURN

            return dataReceived[0]
