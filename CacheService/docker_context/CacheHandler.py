from time import time
from math import floor
import asyncio

from sanic.log import logger

from Client import Client


def errorResult(err, data):
    return {
        'errorMessage': err,
        'content': data
    }


def goodResult(msg, data):
    return {
        'message': msg,
        'content': data
    }


def currentTime():
    return time()


class CacheHandler:
    _QUOTE_CACHE_TIME_LIMIT_SEC = 10

    def __init__(self, redis, RedisHandler, audit, loop, ip, port, LegacyStock):
        self.LegacyStock = LegacyStock
        self.redis = redis
        self.RedisHandler = RedisHandler
        self.audit = audit
        self.client = Client(loop)
        self.dbmURL = f'http://{ip}:{port}'

    async def _getUser(self, user_id):
        check = await self.RedisHandler.rExists(user_id)
        if check:
            data = await self.RedisHandler.rGet(user_id)
            return data
        else:
            result, status = await self.RedisHandler.updateAccountCache(user_id)
            if status == 200:
                data = await self.RedisHandler.rGet(user_id)
                return data, 200
            else:
                return "", 404

    async def getUserFunds(self, user_id):
        result, status = await self._getUser(user_id)
        if status == 200:
            return goodResult(msg="User Data", data=result['account_balance']), 200
        else:
            return result, status

    async def _getStocks(self, user_id, stock_id):
        check = await self.RedisHandler.rExists(f'{user_id}_{stock_id}')
        if check:
            data = await self.RedisHandler.rGet(f'{user_id}_{stock_id}')
            return data
        else:
            result, status = await self.RedisHandler.updateStockCache(user_id, stock_id)
            if status == 200:
                data = await self.RedisHandler.rGet(f'{user_id}_{stock_id}')
                return data, 200
            else:
                return errorResult(f"Couldn't fetch stocks for {user_id}", ""), 404

    async def getUserStocks(self, user_id, stock_id):
        result, status = await self._getStocks(user_id, stock_id)
        if status == 200:
            return goodResult(msg="Stock Data", data=result['stock_amount']), 200
        else:
            return result, status

    async def addFunds(self, trans_num, command, user_id, funds):
        # TODO Update DBM to take trans_num and commands
        data = {
            "user_id": user_id,
            "funds": float(funds)
        }
        result, status = await self.client.postRequest(f"{self.dbmURL}/funds/add_funds", data)
        if status == 200:
            logger.debug(f'{__name__} - Successfully added funds, caching')
            await self.cacheAccountTransaction(data["user_id"])
        return result, status

    async def buyStocks(self, trans_num, command, user_id, stock_symbol, stock_amount, total_value):
        data = {
            "transaction_num": trans_num,
            "command": command,
            "user_id": user_id,
            "stock_id": stock_symbol,
            "amount": total_value,
            "amount_of_stock": stock_amount,
            "time": currentTime()
        }
        await self.RedisHandler.rSet(f"{user_id}_BUY", data)
        return goodResult(msg="Buy created", data=''), 200

    async def sellStocks(self, trans_num, command, user_id, stock_symbol, stock_amount, total_value):
        data = {
            "transaction_num": trans_num,
            "command": command,
            "user_id": user_id,
            "stock_id": stock_symbol,
            "amount": total_value,
            "amount_of_stock": stock_amount,
            "time": currentTime()
        }
        await self.RedisHandler.rSet(f"{user_id}_SELL", data)
        return goodResult(msg="Sell created", data=''), 200

    async def getBuyStocks(self, user_id):
        check = await self.RedisHandler.rExists(f"{user_id}_BUY")
        if check:
            return goodResult(msg="Return buy stock", data=await self.RedisHandler.rGet(f"{user_id}_BUY")), 200
        else:
            logger.info(f'{__name__} - Cannot get stocks for buy for {user_id} as it does not exist in cache')
            return errorResult(err="Buy doesn't exist", data=''), 404

    async def getSellStocks(self, user_id):
        check = await self.RedisHandler.rExists(user_id + "_SELL")
        if check:
            return goodResult(msg="Return sell stock", data=await self.RedisHandler.rGet(f"{user_id}_SELL")), 200
        else:
            logger.info(f'{__name__} - Cannot get stocks for sell for {user_id} as it does not exist in cache')
            return errorResult(err="Sell doesn't exist", data=''), 404

    async def commitBuyStocks(self, trans_num, command, user_id):
        # TODO Update DBM to take trans_num and commands
        buy_request = await self.RedisHandler.rGet(user_id + "_BUY")

        try:
            data = {
                "user_id": user_id,
                "funds": buy_request['amount'],
                "stock_symbol": buy_request['stock_id'],
                "stock_amount": buy_request['amount_of_stock']
            }
            result, status = await self.client.postRequest(f'{self.dbmURL}/stocks/buy_stocks', data)
            if status == 200:
                await self.cacheStockTransaction(user_id, buy_request['stock_id'])
            await self.RedisHandler.rDelete(user_id + "_BUY")
        except:
            err_msg = f'Failed processing data for commit'
            logger.error(f'{err_msg}: Request {buy_request}')
            result, status = await self._failedCommit(trans_num, command, user_id, err_msg)

        return result, status

    async def commitSellStocks(self, trans_num, command, user_id):
        # TODO Update DBM to take trans_num and commands
        sell_request = await self.RedisHandler.rGet(user_id + "_SELL")

        try:
            data = {
                "user_id": user_id,
                "funds": sell_request["amount"],
                "stock_symbol": sell_request["stock_id"],
                "stock_amount": sell_request["amount_of_stock"]
            }
            result, status = await self.client.postRequest(f'{self.dbmURL}/stocks/sell_stocks', data)
            if status == 200:
                await self.cacheStockTransaction(user_id, sell_request['stock_id'])

            await self.RedisHandler.rDelete(user_id + "_SELL")
        except:
            err_msg = f'Failed processing data for commit'
            logger.error(f'{err_msg}: Request {sell_request}')
            result, status = await self._failedCommit(trans_num, command, user_id, err_msg)

        return result, status

    async def _failedCommit(self, trans_num, command, user_id, err_msg):
        await self.audit.handleError(
            trans_num=trans_num,
            command=command,
            error_msg=err_msg,
            user_id=user_id,
        )
        return errorResult(err=err_msg, data=''), 404

    async def cacheAccountTransaction(self, user_id, max_retry=5):
        retry = 1
        while retry <= max_retry:
            logger.debug(
                f'{__name__} - Attempt {retry}/{max_retry} to cache transaction for {user_id} --> account info')
            account_result, account_status = await self.RedisHandler.updateAccountCache(user_id)
            if account_status == 200:
                return
            retry += 1

    async def cacheStockTransaction(self, user_id, stock_symbol, max_retry=5):
        retry = 1
        while retry <= max_retry:
            logger.debug(
                f'{__name__} - Attempt {retry}/{max_retry} to cache transaction for {user_id} --> {stock_symbol}')
            account_result, account_status = await self.RedisHandler.updateAccountCache(user_id)
            stock_result, stock_status = await self.RedisHandler.updateStockCache(user_id, stock_symbol)
            if account_status == 200 and stock_status == 200:
                return
            retry += 1

    async def cancelBuy(self, trans_num, command, user_id):
        result = await self.RedisHandler.rExists(user_id + "_BUY")
        if result:
            await self.RedisHandler.rDelete(user_id + "_BUY")
            return goodResult(msg="Buy Cancelled", data=''), 200
        else:
            err_msg = "No buy request exists"
            logger.info(
                f'{__name__} - Cannot cancel buy for {user_id} as it does not exist in cache - {trans_num} - {command}')
            return errorResult(err=err_msg, data=''), 404

    async def cancelSell(self, trans_num, command, user_id):
        result = await self.RedisHandler.rExists(user_id + "_SELL")
        if result:
            await self.RedisHandler.rDelete(user_id + "_SELL")
            return goodResult(msg="Sell Cancelled", data=''), 200
        else:
            err_msg = "No sell request exists"
            logger.info(
                f'{__name__} - Cannot cancel sell for {user_id} as it does not exist in cache - {trans_num} - {command}')
            return errorResult(err=err_msg, data=''), 404

    async def getQuote(self, trans_num, user_id, stock_id):
        check = await self.RedisHandler.rExists(stock_id)
        if check:
            quote = await self.RedisHandler.rGet(stock_id)

            then = float(quote['time'])
            now = currentTime()
            difference = (now - then)
            if difference <= self._QUOTE_CACHE_TIME_LIMIT_SEC:
                logger.debug(f'{__name__} - Cache hit while getting stock {stock_id}')
                return goodResult(msg="Quote price", data={'price': quote['price']}), 200

        result, status = await self.LegacyStock.getQuote(trans_num, user_id, stock_id)
        if status == 200:
            return goodResult(msg="Quote price", data=result), 200

        else:
            logger.error(
                f'{__name__} - Cannot get quote for {trans_num}, {user_id}, {stock_id} due to an error. '
                f'{status} --> {result}')
            self.audit.handleError(
                trans_num=trans_num,
                command='QUOTE',
                error_msg=f'Error getting quote - {result} ({status})',
                user_id=user_id,
                stock_symbol=stock_id
            )
            return result, status

    async def getBulkQuote(self, user_ids, stock_ids, transaction_nums):
        results = []
        while stock_ids:
            user_id = user_ids.pop(0)
            stock_id = stock_ids.pop(0)
            transaction_num = transaction_nums.pop(0)

            result, status = await self.getQuote(transaction_num, user_id, stock_id)

            if status != 200:
                continue

            formattedResult = {'stock_id': stock_id, 'price': result['content']}
            results.append(formattedResult)

        return results, 200

    async def setBuyAmount(self, data):
        result, status = await self.client.postRequest(f'{self.dbmURL}/triggers/buy/set/amount', data)
        if status == 200:
            await self.cacheAccountTransaction(data["user_id"])
        return result, status

    async def setSellAmount(self, data):
        result, status = await self.client.postRequest(f'{self.dbmURL}/triggers/sell/set/amount', data)
        if status == 200:
            await self.cacheStockTransaction(data['user_id'], data['stock_symbol'])
        return result, status

    async def executeTriggers(self, data):

        tasks = [asyncio.create_task(self.__executeTriggers(operation)) for operation in data]
        results = await asyncio.gather(*tasks)

        failedOperations = []
        for operationResult in results:
            for result, status in operationResult:
                if status == 200:
                    continue
                else:
                    failedOperations.append(result['content'])

        # no idea how we want to handle failures.
        return goodResult("finished", ''), 200

    async def __executeTriggers(self, operation):
        command = operation['trigger']

        if command == "BUY_TRIGGER":
            result, status = await self.__executeBuyTrigger(command, operation)

        elif command == "SELL_TRIGGER":
            result, status = await self.__executeSellTrigger(command, operation)

        else:
            result, status = errorResult("not a valid trigger command", operation), 500

        return result, status

    async def __executeBuyTrigger(self, command, operation):
        user, status = await self._getUser(operation['user_id'])
        if status != 200:
            return errorResult("User seemingly doesn't exist", operation), 404

        reservedFunds = float(user['reserved_balance'])
        executionPrice = float(operation['executed_at'])
        stockAmount = floor(reservedFunds / executionPrice)
        funds = round(stockAmount * executionPrice, 2)

        data = {
            "user_id": operation['user_id'],
            "funds": funds,
            "stock_symbol": operation['stock_symbol'],
            "stock_amount": stockAmount,
            "transaction_num": operation['transaction_num']
        }

        result, status = await self.client.postRequest(f'{self.dbmURL}/triggers/execute/buy', data)
        if status == 200:
            await self.cacheStockTransaction(data['user_id'], data['stock_symbol'])

        else:
            logger.error(f'{__name__} - error during execution for trigger buy {operation["transaction_num"]}')
            self.audit.handleError(
                trans_num=operation['transaction_num'],
                command=command,
                error_msg=f'error posting buy trigger execute',
                user_id=operation['user_id'],
                stock_symbol=operation['stock_symbol']
            )
            return errorResult("post request to DBM failed", operation), 500

        return goodResult("finished", operation), 200

    async def __executeSellTrigger(self, command, operation):
        stockBal, status = await self._getStocks(operation['user_id'], operation['stock_symbol'])
        if status != 200:
            return errorResult("User doesn't hold any stock", stockBal), 404

        reservedStock = float(stockBal['stock_reserved'])
        executionPrice = float(operation['executed_at'])
        funds = round(reservedStock * executionPrice, 2)

        data = {
            "user_id": operation['user_id'],
            "funds": funds,
            "stock_symbol": operation['stock_symbol'],
            "stock_amount": reservedStock,
            "transaction_num": operation['transaction_num']
        }

        result, status = await self.client.postRequest(f'{self.dbmURL}/triggers/execute/sell', data)
        if status == 200:
            await self.cacheStockTransaction(data['user_id'], data['stock_symbol'])

        else:
            logger.error(f'{__name__} - error during execution for trigger sell {operation["transaction_num"]}')
            self.audit.handleError(
                trans_num=operation['transaction_num'],
                command=command,
                error_msg=f'error posting buy trigger execute',
                user_id=operation['user_id'],
                stock_symbol=operation['stock_symbol']
            )
            return errorResult("post request to DBM failed", result), 500

        return goodResult("finished", operation), 200

    # __________________________________________________________________________________________________________________
