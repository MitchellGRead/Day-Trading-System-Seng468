from time import time

import aiohttp
from sanic.log import logger
from Client import Client

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

    def __init__(self, service_name, ip, port, loop):
        self.client = Client(loop)
        self.service_name = service_name
        self.url = f'http://{ip}:{port}'

    async def closeClient(self):
        await self.client.stop()

    def baseEvent(self, trans_num, command):
        return {
            'server': self.service_name,
            'timestamp': currentTimeMs(),
            'transaction_num': trans_num,
            'command': command
        }

    async def handleUserCommand(self, trans_num, command, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        resp = await self.client.postRequest(f'{self.url}/event/user_command', event)
        logger.debug(resp)
        return

    async def handleError(self, trans_num, command, error_msg, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            'error_msg': error_msg,
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        resp = await self.client.postRequest(f'{self.url}/event/error', event)
        logger.debug(resp)
        return

    async def handleSystem(self, trans_num, command, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        resp = await self.client.postRequest(f'{self.url}/event/system', event)
        logger.debug(resp)
        return
