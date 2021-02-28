from time import time
from math import ceil, floor

import aiohttp


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

    # TO DO:
    # VERIFICATION OF DATA RECEIVED FROM CACHE?
    # AUDIT
    # RECHECK PRICE ON COMMIT

    def __init__(self, audit, client, ip, port):
        self.audit = audit
        self.client = client
        self.cacheURL = f'http://{ip}:{port}'

    async def addFunds(self, trans_num, user_id, amount):
        data = {'transaction_num': trans_num, 'user_id': user_id, 'funds': float(amount)}
        result, status = await self.postRequest(f"{self.cacheURL}/funds/add_funds", data)
        return result, status

    async def getQuote(self, trans_num, user_id, stock_id):
        result, status = await self.getRequest(f"{self.cacheURL}/quote/get/{user_id}/{stock_id}/{trans_num}")
        return result, status

    async def buyStock(self, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status == 200:
            quotePrice = float(result['content']['price'])
            if float(quotePrice) > float(amount):
                err_msg = "Not enough capital to buy this stock."
                await self.audit.handleError(trans_num, 'BUY', err_msg, user_id, stock_symbol, amount)
                return errorResult(err=err_msg, data=''), 400

            totalStock = floor(float(amount)/float(quotePrice))
            totalValue = round(quotePrice*totalStock, 2)
            result, status = await self.getRequest(f"{self.cacheURL}/funds/get/user/{user_id}")
            if status == 200:
                userBal = result['content']

                if totalValue > float(userBal):
                    err_msg = "User doesn't have required funds"
                    await self.audit.handleError(trans_num, 'BUY', err_msg, user_id, stock_symbol, amount)
                    return errorResult(err=err_msg, data=''), 400

                data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol, 'stock_amount': totalStock, 'funds': totalValue}
                result, status = await self.postRequest(f"{self.cacheURL}/stocks/buy_stocks", data)
                return result, status
            else:
                return result, status
        else:
            return result, status

    async def getBuy(self, user_id):
        result, status = await self.getRequest(f"{self.cacheURL}/stocks/get_buy/{user_id}")
        return result, status

    async def commitBuy(self, trans_num, user_id):
        result, status = await self.getBuy(user_id)
        if status == 200:
            check = result['content']
            data = {'transaction_num': trans_num, 'user_id': user_id}
            then = float(check['time'])
            now = currentTime()
            difference = (now-then)
            if difference < 60:
                result, status = await self.postRequest(f"{self.cacheURL}/stocks/commit_buy", data)
                return result, status
            else:
                err_msg = "Previous buy has expired"
                await self.audit.handleError(trans_num, 'COMMIT_BUY', err_msg, user_id)
                return errorResult(err=err_msg, data=''), 400
        else:
            return result, status

    async def cancelBuy(self, trans_num, user_id):
        data = {'transaction_num': trans_num, 'user_id': user_id}
        result, status = await self.postRequest(f"{self.cacheURL}/stocks/cancel_buy", data)
        return result, status

    async def sellStock(self, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status == 200:
            quotePrice = float(result['content']['price'])
            totalStock = ceil(float(amount) / float(quotePrice))
            totalValue = round(quotePrice * totalStock, 2)
            result, status = await self.getRequest(f"{self.cacheURL}/stocks/get/user/{user_id}/{stock_symbol}")
            if status == 200:
                stockBal = result['content']
                if totalStock > stockBal:
                    err_msg = "User doesn't have required stocks"
                    await self.audit.handleError(trans_num, 'SELL', err_msg, user_id)
                    return errorResult(err="User doesn't have required stocks", data=''), 400

                data = {'transaction_num': trans_num, 'user_id': user_id, 'stock_symbol': stock_symbol,
                        'stock_amount': totalStock, 'funds': totalValue}
                result, status = await self.postRequest(self.cacheURL + "/stocks/sell_stocks", data)
                return result, status
            else:
                return result, status
        else:
            return result, status

    async def getSell(self, user_id):
        result, status = await self.getRequest(f"{self.cacheURL}/stocks/get_sell/{user_id}")
        return result, status

    async def commitSell(self, trans_num, user_id):
        result, status = await self.getSell(user_id)
        if status == 200:
            check = result['content']
            data = {'transaction_num': trans_num, 'user_id': user_id}
            then = float(check['time'])
            now = currentTime()
            difference = (now - then)
            if difference < 60:
                result, status = await self.postRequest(f"{self.cacheURL}/stocks/commit_sell", data)
                return result, status
            else:
                err_msg = "Previous sell has expired"
                await self.audit.handleError(trans_num, 'COMMIT_SELL', err_msg, user_id)
                return errorResult(err=err_msg, data=''), 400
        else:
            return result, status

    async def cancelSell(self, trans_num, user_id):
        data = {'transaction_num': trans_num, 'user_id': user_id}
        result, status = await self.postRequest(f"{self.cacheURL}/stocks/cancel_sell", data)
        return result, status

    # __________________________________________________________________________________________________________________

    async def getRequest(self, url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                js = await resp.json()
                status = resp.status
                return js, status

    async def postRequest(self, url, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                js = await resp.json()
                status = resp.status
                return js, status
