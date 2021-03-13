from Client import Client
from sanic.log import logger
import sys

from TriggerExecutionManager import TriggerExecutionManager


class TriggerHandler:

    def __init__(self, audit, cache_ip, cache_port, loop):
        self.audit = audit
        self.cache_url = f'http://{cache_ip}:{cache_port}'
        self.client = Client(loop)

    def convertCommand(self, command):
        res = ''
        if command == 'SET_BUY_TRIGGER':
            res = TriggerExecutionManager.BUY
        elif command == 'SET_SELL_TRIGGER':
            res = TriggerExecutionManager.SELL
        return res

    def toTriggers(self, triggers_data):
        triggers = []
        for data in triggers_data:
            trigger = self.toTrigger(data)
            if trigger is not None:
                triggers.append(trigger)
        return triggers

    def toTrigger(self, trigger_data):
        try:
            trigger = {
                'transaction_num': trigger_data['transaction_num'],
                'trigger': self.convertCommand(trigger_data['command']),
                'user_id': trigger_data['user_id'],
                'stock_symbol': trigger_data['stock_symbol'],
                'trigger_price': trigger_data['trigger_price']
            }
        except KeyError:
            logger.error(f'Invalid key when converting data to trigger --> {trigger_data}')
            return None
        else:
            return trigger

    async def fetchActiveTriggers(self):
        endpoint = '/triggers/get/active'
        results, status = await self.client.getRequest(f'{self.cache_url}{endpoint}')
        if status != 200 or results is None:
            logger.error(f'Failed to fetch existing triggers from database. Service shutting down.')
            sys.exit(1)

        triggers = self.toTriggers(results)
        return triggers

    async def setBuyAmount(self, trans_num, command, user_id, stock_symbol, amount):
        # TODO make POST request to cache service endpoint
        pass

    async def setBuyTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        # TODO make POST request to cache service endpoint
        # TODO return trigger object for the execution manager
        pass

    async def cancelBuyTrigger(self, trans_num, command, user_id, stock_symbol):
        # TODO make POST request to cache service endpoint
        # TODO return trigger object for removal in execution manager
        pass

    async def setSellAmount(self, trans_num, command, user_id, stock_symbol, amount):
        # TODO make POST request to cache service endpoint
        pass

    async def setSellTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        # TODO make POST request to cache service endpoint
        # TODO return trigger object for the execution manager
        pass

    async def cancelSellTrigger(self, trans_num, command, user_id, stock_symbol):
        # TODO make POST request to cache service endpoint
        # TODO return trigger object for removal in execution manager
        pass
