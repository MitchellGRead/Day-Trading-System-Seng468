from time import time
from math import ceil, floor
from Client import Client
from sanic.log import logger


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


class TransactionHandler:
    TRANSACTION_TIME_LIMIT = 60

    # TO DO:
    # VERIFICATION OF DATA RECEIVED FROM CACHE?
    # AUDIT
    # RECHECK PRICE ON COMMIT

    def __init__(self, audit, ip, port, loop):
        self.audit = audit
        self.client = Client(loop)
        self.cacheURL = f'http://{ip}:{port}'

    async def addFunds(self, trans_num, user_id, amount, command):
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'amount': amount,
            'command': command
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/funds/add_funds", data)
        return result, status

    async def getQuote(self, trans_num, user_id, stock_symbol):
        result, status = await self.client.getRequest(f"{self.cacheURL}/quote/get/{user_id}/{stock_symbol}/{trans_num}")
        return result, status

    async def buyStock(self, command, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get quote --> {result} - {status}')
            return result, status

        quote_price = float(result['content']['price'])

        if quote_price > amount:
            err_msg = "Not enough capital to buy this stock."
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {quote_price} > {amount}')
            await self.audit.handleError(trans_num, command, err_msg, user_id, stock_symbol, amount)
            return errorResult(err=err_msg, data=''), 400

        total_stock = floor(amount / quote_price)
        total_value = round(quote_price * total_stock, 2)

        # get user funds from cache
        result, status = await self.client.getRequest(f"{self.cacheURL}/funds/get/user/{user_id}")
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
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'stock_amount': total_stock,
            'funds': total_value
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/stocks/buy_stocks", data)
        return result, status

    async def getBuy(self, user_id):
        result, status = await self.client.getRequest(f"{self.cacheURL}/stocks/get_buy/{user_id}")
        return result, status

    async def commitBuy(self, command, trans_num, user_id):
        result, status = await self.getBuy(user_id)
        if status != 200:
            err_msg = 'No BUY exists to commit'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
            return result, status

        then = float(result['content']['time'])
        now = currentTime()
        difference = (now - then)

        if difference > self.TRANSACTION_TIME_LIMIT:
            err_msg = "Previous buy has expired"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {difference} > {self.TRANSACTION_TIME_LIMIT}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err=err_msg, data=''), 400

        data = {
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/stocks/commit_buy", data)
        return result, status

    async def cancelBuy(self, trans_num, user_id, command):
        data = {
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/stocks/cancel_buy", data)
        if status != 200:
            err_msg = 'Could not cancel sell as no SELL command exists'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
        return result, status

    async def sellStock(self, command, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get quote --> {result} - {status}')
            return result, status
        quote_price = float(result['content']['price'])

        result, status = await self.client.getRequest(f"{self.cacheURL}/stocks/get/user/{user_id}/{stock_symbol}")
        if status != 200:
            logger.info(f'{command} - {trans_num} - {user_id} --> failed to get user stocks --> {result} - {status}')
            return result, status

        total_stock = ceil(amount / quote_price)
        total_value = round(quote_price * total_stock, 2)
        stock_bal = result['content']
        if total_stock > stock_bal:
            err_msg = "User doesn't have required stocks"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {total_stock} > {stock_bal}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err="User doesn't have required stocks", data=''), 400

        data = {
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'stock_amount': total_stock,
            'funds': total_value
        }
        result, status = await self.client.postRequest(f'{self.cacheURL}/stocks/sell_stocks', data)
        return result, status

    async def getSell(self, user_id):
        result, status = await self.client.getRequest(f"{self.cacheURL}/stocks/get_sell/{user_id}")
        return result, status

    async def commitSell(self, command, trans_num, user_id):
        result, status = await self.getSell(user_id)
        if status != 200:
            err_msg = 'No BUY exists to commit'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
            return result, status

        then = float(result['content']['time'])
        now = currentTime()
        difference = (now - then)
        if difference > self.TRANSACTION_TIME_LIMIT:
            err_msg = "Previous sell has expired"
            logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} {difference} > {self.TRANSACTION_TIME_LIMIT}')
            await self.audit.handleError(trans_num, command, err_msg, user_id)
            return errorResult(err=err_msg, data=''), 400

        data = {
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/stocks/commit_sell", data)
        return result, status

    async def cancelSell(self, trans_num, user_id, command):
        data = {
            'command': command,
            'transaction_num': trans_num,
            'user_id': user_id
        }
        result, status = await self.client.postRequest(f"{self.cacheURL}/stocks/cancel_sell", data)
        if status != 200:
            err_msg = 'Could not cancel sell as no SELL command exists'
            await self.auditNoCommand(command, trans_num, user_id, result, status, err_msg)
        return result, status

    async def auditNoCommand(self, command, trans_num, user_id, result, status, err_msg):
        logger.info(f'{command} - {trans_num} - {user_id} --> {err_msg} --> {result} - {status}')
        self.audit.handleError(trans_num, command, err_msg, user_id)

    # __________________________________________________________________________________________________________________
