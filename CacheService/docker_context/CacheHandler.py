from time import time
from math import floor, ceil
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
    TRANSACTION_TIME_LIMIT = 60

    def __init__(self, redis, RedisHandler, audit, loop, ip, port, LegacyStock):
        self.LegacyStock = LegacyStock
        self.redis = redis
        self.RedisHandler = RedisHandler
        self.audit = audit
        self.client = Client(loop)
        self.dbmURL = f'http://{ip}:{port}'

    async def auditNoCommand(self, command, trans_num, user_id, result, status, err_msg):
        logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} --> {result} - {status}')
        await self.audit.handleError(trans_num, command, err_msg, user_id)

    async def _getUser(self, user_id):
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
        result, status = await self.RedisHandler.updateStockCache(user_id, stock_id)
        if status == 200:
            data = await self.RedisHandler.rGet(f'{user_id}_{stock_id}')
            return data, 200
        else:
            return errorResult(f"Couldn't fetch stocks for {user_id} - {stock_id}", ""), 404

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

    async def buyStocks(self, trans_num, command, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get quote --> {result} - {status}')
            return result, status

        quotedPrice = float(result['content'])

        if quotedPrice > amount:
            err_msg = "Not enough capital to buy this stock."
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {quotedPrice} > {amount}')
            await self.audit.handleError(trans_num, command, err_msg, user_id, stock_symbol, amount)
            return errorResult(err=err_msg, data=''), 400

        total_stock = floor(amount/quotedPrice)
        total_value = round(quotedPrice*total_stock, 2)

        result, status = await self.getUserFunds(user_id)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get user funds --> {result} - {status}')
            return result, status

        user_bal = float(result['content'])

        if total_value > user_bal:
            err_msg = "User doesn't have required funds"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {total_value} > {user_bal}')
            await self.audit.handleError(trans_num, command, err_msg, user_id, stock_symbol, amount)
            return errorResult(err=err_msg, data=''), 400

        data = {
            "transaction_num": trans_num,
            "command": command,
            "user_id": user_id,
            "stock_id": stock_symbol,
            "amount": total_value,
            "amount_of_stock": total_stock,
            "time": currentTime()
        }
        await self.RedisHandler.rSet(f"{user_id}_BUY", data)
        return goodResult(msg="Buy created", data=''), 200

    async def sellStocks(self, trans_num, command, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get quote --> {result} - {status}')
            return result, status

        quotedPrice = float(result['content'])

        total_stock = ceil(amount / quotedPrice)
        total_value = round(quotedPrice * total_stock, 2)

        result, status = await self.getUserStocks(user_id, stock_symbol)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get user stocks --> {result} - {status}')
            return result, status

        stock_bal = result['content']
        if total_stock > stock_bal:
            err_msg = "User doesn't have required stocks"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {total_stock} > {stock_bal}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err="User doesn't have required stocks", data=''), 400

        data = {
            "transaction_num": trans_num,
            "command": command,
            "user_id": user_id,
            "stock_id": stock_symbol,
            "amount": total_value,
            "amount_of_stock": total_stock,
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
        result, status = await self.getBuyStocks(user_id)
        if status != 200:
            err_msg = 'No BUY exists to commit'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
            return result, status

        buy_request = result['content']

        then = buy_request['time']
        now = currentTime()
        difference = (now-then)

        if difference > self.TRANSACTION_TIME_LIMIT:
            err_msg = "Previous buy has expired"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {difference} > {self.TRANSACTION_TIME_LIMIT}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err=err_msg, data=''), 400

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
        result, status = await self.getSellStocks(user_id)
        if status != 200:
            err_msg = 'No SELL exists to commit'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
            return result, status

        sell_request = result['content']

        then = sell_request['time']
        now = currentTime()
        difference = (now-then)

        if difference > self.TRANSACTION_TIME_LIMIT:
            err_msg = "Previous sell has expired"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {difference} > {self.TRANSACTION_TIME_LIMIT}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err=err_msg, data=''), 400

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
