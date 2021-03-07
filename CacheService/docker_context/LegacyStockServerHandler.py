import socket
from time import sleep
from sanic.log import logger
import asyncio


class LegacyStockServerHandler:

    def __init__(self, ip, port, audit):
        self.ip = ip
        self.port = port
        self.audit = audit

    async def quoteSocket(self):
        stockSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug("Attempting Connection to Quote Server")
        while stockSocket.connect_ex((self.ip, self.port)) != 0:
            await asyncio.sleep(1)
        logger.debug("Quote Connection Started")
        return stockSocket

    async def getQuote(self, trans_num, user_id, stock_symbol):
        stockSocket = await self.quoteSocket()
        message = "{},{}\n".format(stock_symbol, user_id)
        stockSocket.send(message.encode())
        dataReceived = stockSocket.recv(1024).decode().split(",")
        stockSocket.close()

        price, _, _, quote_time, cryptokey = dataReceived
        price = float(price)
        quote_time = int(quote_time)
        result = {
            "transaction_num": trans_num,
            "user_id": user_id,
            "stock_symbol": stock_symbol,
            "price": price,
            "cryptokey": cryptokey,
            "quoteTime": quote_time
        }

        await self.audit.handleQuote(trans_num, user_id, stock_symbol, price, quote_time, cryptokey)
        # DO FAILURE
        return {'price': price}, 200
