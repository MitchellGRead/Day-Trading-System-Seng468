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

    # __________________________________________________________________________________________________________________
