import asyncio
from time import time

from sanic.log import logger


def currentTime():
    return time()


class LegacyStockServerHandler:
    _QUOTE_CACHE_TIME_LIMIT_SEC = 10

    def __init__(self, ip, port, audit, redisHandler):
        self.ip = ip
        self.port = port
        self.audit = audit
        self.RedisHandler = redisHandler
        self.__tracker = {}

    async def quoteSocket(self):
        logger.info(f"{__name__} - Attempting Connection to Quote Server")
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        logger.info(f"{__name__} - Quote Connection Started")
        return reader, writer

    async def getQuote(self, trans_num, user_id, stock_symbol):
        if stock_symbol in self.__tracker.keys():
            runningTask = self.__tracker[stock_symbol]
            while not runningTask.done():
                await asyncio.sleep(1)
            check = await self.RedisHandler.rExists(stock_symbol)
            if check:
                quote = await self.RedisHandler.rGet(stock_symbol)
                return quote['price'], 200
            else:
                return await self.__newQuoteTask(trans_num, user_id, stock_symbol)
        else:
            return await self.__newQuoteTask(trans_num, user_id, stock_symbol)

    async def __newQuoteTask(self, trans_num, user_id, stock_symbol):
        newTask = asyncio.create_task(self.__getQuoteFunc(trans_num, user_id, stock_symbol))
        self.__tracker[stock_symbol] = newTask
        await newTask

        quote = await self.RedisHandler.rGet(stock_symbol)
        return quote['price'], 200

    async def __getQuoteFunc(self, trans_num, user_id, stock_symbol):
        reader, writer = await self.quoteSocket()

        message = f'{stock_symbol},{user_id}\n'
        writer.write(message.encode())
        await writer.drain()

        data_received = await reader.read(1024)

        logger.info(f"{__name__} - Closing connection")
        writer.close()
        await writer.wait_closed()

        price, _, _, quote_time, cryptokey = data_received.decode().split(',')
        price = float(price)
        quote_time = int(quote_time)

        await self.audit.handleQuote(int(trans_num), user_id, stock_symbol, price, quote_time, cryptokey)
        # TODO: Failure.

        await self.RedisHandler.rSet(stock_symbol, {'stock_id': stock_symbol, 'price': price, 'time': currentTime()})
        del self.__tracker[stock_symbol]

        return


