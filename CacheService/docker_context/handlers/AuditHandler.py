from time import time

import aiohttp
from sanic.log import logger


def currentTimeMs():
    return round(time() * 1000)


def addKeyValuePairs(user_id='', stock_symbol='', amount=0, filename=''):
    res = {}
    if user_id:
        res['user_id'] = user_id
    if stock_symbol:
        res['stock_symbol'] = stock_symbol
    if amount:
        res['amount'] = amount
    if filename:
        res['filename'] = filename
    return res


class AuditHandler:

    def __init__(self, client, service_name, ip, port):
        self.client = client
        self.service_name = service_name
        self.url = f'http://{ip}:{port}'

    def baseEvent(self, trans_num, command=''):  # command is optional only for quote events
        event = {
            'server': self.service_name,
            'timestamp': currentTimeMs(),
            'transaction_num': trans_num,
        }
        if command:
            event['command'] = command
        return event

    async def handleError(self, trans_num, command, error_msg, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            'error_msg': error_msg,
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        resp = await self.postRequest('/event/error', event)
        logger.debug(resp)
        return

    async def handleSystem(self, trans_num, command, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        resp = await self.postRequest('/event/system', event)
        logger.debug(resp)
        return

    async def handleQuote(self, trans_num, user_id, stock_symbol, price, quote_server_time, crptokey):
        event = {
            **self.baseEvent(trans_num),
            **addKeyValuePairs(user_id, stock_symbol),
            'price': price,
            'quote_server_timestamp': quote_server_time,
            'cryptokey': crptokey
        }

        resp = await self.postRequest('/event/quote', event)
        logger.debug(resp)
        return

    async def postRequest(self, endpoint, data):
        url = f'{self.url}{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                js = await resp.json()
                return js
