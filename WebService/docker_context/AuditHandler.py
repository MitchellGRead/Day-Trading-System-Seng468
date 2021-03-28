from time import time

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

    def baseEvent(self, trans_num, command):
        return {
            'server': self.service_name,
            'timestamp': currentTimeMs(),
            'transaction_num': trans_num,
            'command': command
        }

    async def handleDisplaySummary(self, trans_num, command, user_id):
        endpoint = f'/get/{command}/trans/{trans_num}/user/{user_id}'
        logger.debug(f'Getting display summary - {trans_num} - {user_id}')
        resp, status = await self.client.getRequest(f'{self.url}{endpoint}')
        return resp, status

    async def handleUserCommand(self, trans_num, command, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        logger.debug(f'Auditing user command - {trans_num} - {user_id}')
        resp = await self.client.postRequest(f'{self.url}/event/user_command', event)
        logger.debug(f'Audit response - {resp}')
        return

    async def handleError(self, trans_num, command, error_msg, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            'error_msg': error_msg,
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        logger.debug(f'Auditing error event - {trans_num} - {user_id}')
        resp = await self.client.postRequest(f'{self.url}/event/error', event)
        logger.debug(f'Audit response - {resp}')
        return

    async def handleSystem(self, trans_num, command, user_id='', stock_symbol='', amount=0, filename=''):
        event = {
            **self.baseEvent(trans_num, command),
            **addKeyValuePairs(user_id, stock_symbol, amount, filename)
        }

        logger.debug(f'Auditing system event - {trans_num} - {user_id}')
        resp = await self.client.postRequest(f'{self.url}/event/system', event)
        logger.debug(f'Audit response - {resp}')
        return
