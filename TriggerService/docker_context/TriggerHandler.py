from Client import Client
from sanic.log import logger
import sys

from TriggerExecutionManager import TriggerExecutionManager


class TriggerHandler:

    def __init__(self, audit, dbm_ip, dbm_port, loop):
        self.audit = audit
        self.dbm_url = f'http://{dbm_ip}:{dbm_port}'
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
                'stock_symbol': trigger_data['stock_id'],
                'stock_amount': trigger_data['stock_amount'],
                'trigger_price': trigger_data['trigger_price']
            }
        except KeyError:
            logger.error(f'Invalid key when converting data to trigger --> {trigger_data}')
            return None
        else:
            return trigger

    async def fetchExistingTriggers(self):
        triggers = []
        # TODO waiting on DBM additions
        return triggers

    async def setBuyAmount(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/buy/set/amount'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'amount': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set buy amount call to DBM: {results}')
            return "setBuyAmount failed on DBM call", 500
        return "Success", 200

    async def setBuyTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/buy/set/price'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'price': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set buy trigger call to DBM: {results}')
            return "setBuyTrigger failed on DBM call", 500

        trigger_data = results
        trigger_data['command'] = 'SET_BUY_TRIGGER'
        trigger_data['trigger_price'] = trigger_data.pop('price')
        trigger = self.toTrigger(trigger_data)
        return trigger, 200

    async def cancelBuyTrigger(self, trans_num, command, user_id, stock_symbol):
        endpoint = '/triggers/buy/cancel'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during cancel buy trigger call to DBM: {results}')
            return "cancelBuyTrigger failed on DBM call", 500
        return "Trigger removed", 200

    async def setSellAmount(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/sell/set/amount'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'amount': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set sell amount call to DBM: {results}')
            return "setSellAmount failed on DBM call", 500
        return "Success", 200

    async def setSellTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/sell/set/price'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'price': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set sell trigger call to DBM: {results}')
            return "setSellTrigger failed on DBM call", 500

        trigger_data = results
        trigger_data['command'] = 'SET_SELL_TRIGGER'
        trigger_data['trigger_price'] = trigger_data.pop('price')
        trigger = self.toTrigger(trigger_data)
        return trigger, 200

    async def cancelSellTrigger(self, trans_num, command, user_id, stock_symbol):
        endpoint = '/triggers/sell/cancel'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during cancel sell trigger call to DBM: {results}')
            return "cancelSellTrigger failed on DBM call", 500
        return "Trigger removed", 200
