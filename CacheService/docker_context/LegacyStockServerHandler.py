import asyncio

from sanic.log import logger


class LegacyStockServerHandler:

    def __init__(self, ip, port, audit):
        self.ip = ip
        self.port = port
        self.audit = audit

    async def quoteSocket(self):
        logger.info(f"{__name__} - Attempting Connection to Quote Server")
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        logger.info(f"{__name__} - Quote Connection Started")
        return reader, writer

    async def getQuote(self, trans_num, user_id, stock_symbol):
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

        await self.audit.handleQuote(trans_num, user_id, stock_symbol, price, quote_time, cryptokey)
        # DO FAILURE
        return {'price': price}, 200
