from Client import Client
from sanic.log import logger
import sys

from TriggerExecutionManager import TriggerExecutionManager


class TriggerHandler:

    def __init__(self, audit, dbm_ip, dbm_port, cache_ip, cache_port, loop):
        self.audit = audit
        self.dbm_url = f'http://{dbm_ip}:{dbm_port}'
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
        triggers_data = []
        endpoint = '/triggers/all/get'
        results, status = await self.client.getRequest(f'{self.dbm_url}{endpoint}')

        if status == 200 and results != []:
            for stock_id in results.keys():
                stockObj = results[stock_id]
                if 'buy_triggers' in stockObj:
                    buyObj = stockObj['buy_triggers']
                    for user_id in buyObj.keys():
                        trigger = {'stock_symbol': stock_id, 'user_id': user_id, 'command': 'SET_BUY_TRIGGER'}

                        infoObj = buyObj[user_id]
                        trigger['stock_amount'] = infoObj[0]
                        trigger['trigger_price'] = infoObj[1]
                        trigger['transaction_num'] = infoObj[2]
                        triggers_data.append(trigger)

                if 'sell_triggers' in stockObj:
                    sellObj = stockObj['sell_triggers']
                    for user_id in sellObj.keys():
                        trigger = {'stock_symbol': stock_id, 'user_id': user_id, 'command': 'SET_SELL_TRIGGER'}

                        infoObj = sellObj[user_id]
                        trigger['stock_amount'] = infoObj[0]
                        trigger['trigger_price'] = infoObj[1]
                        trigger['transaction_num'] = infoObj[2]
                        triggers_data.append(trigger)

        triggers = self.toTriggers(triggers_data)
        return triggers

    async def updateCacheFunds(self, user_id):
        endpoint = '/update/user'
        data = {'user_id': user_id}
        result, status = await self.client.postRequest(f'{self.cache_url}{endpoint}', data)
        return

    async def updateCacheStocks(self, user_id, stock_symbol):
        endpoint = '/update/stock'
        data = {'user_id': user_id, 'stock_symbol': stock_symbol}
        result, status = await self.client.postRequest(f'{self.cache_url}{endpoint}', data)
        return

    async def setBuyAmount(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/buy/set/amount'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'amount': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set buy amount call to DBM: {results}')
            return "setBuyAmount failed on DBM call", 404
        return "Success", 200

    async def setBuyTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/buy/set/price'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'price': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set buy trigger call to DBM: {results}')
            return "setBuyTrigger failed on DBM call", 404

        await self.updateCacheFunds(user_id)

        replace = results['replace']
        # replace = True if 'true' in replace else False

        trigger_data = results
        trigger_data['command'] = 'SET_BUY_TRIGGER'
        trigger_data['trigger_price'] = trigger_data.pop('price')
        trigger = self.toTrigger(trigger_data)
        return [trigger, replace], 200

    async def cancelBuyTrigger(self, trans_num, command, user_id, stock_symbol):
        endpoint = '/triggers/buy/cancel'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during cancel buy trigger call to DBM: {results}')
            return "cancelBuyTrigger failed on DBM call", 404

        await self.updateCacheFunds(user_id)

        return "Trigger removed", 200

    async def setSellAmount(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/sell/set/amount'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'amount': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set sell amount call to DBM: {results}')
            return "setSellAmount failed on DBM call", 404
        return "Success", 200

    async def setSellTrigger(self, trans_num, command, user_id, stock_symbol, amount):
        endpoint = '/triggers/sell/set/price'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'price': amount}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during set sell trigger call to DBM: {results}')
            return "setSellTrigger failed on DBM call", 404

        await self.updateCacheStocks(user_id, stock_symbol)

        replace = results['replace']
        # replace = True if 'true' in replace else False

        trigger_data = results
        trigger_data['command'] = 'SET_SELL_TRIGGER'
        trigger_data['trigger_price'] = trigger_data.pop('price')
        trigger = self.toTrigger(trigger_data)
        return [trigger, replace], 200

    async def cancelSellTrigger(self, trans_num, command, user_id, stock_symbol):
        endpoint = '/triggers/sell/cancel'
        data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol}

        results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', data)
        if status != 200 or results is None:
            logger.error(f'Failed during cancel sell trigger call to DBM: {results}')
            return "cancelSellTrigger failed on DBM call", 404

        await self.updateCacheStocks(user_id, stock_symbol)

        return "Trigger removed", 200
