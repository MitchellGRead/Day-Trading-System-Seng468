from time import time
from math import ceil, floor
from sanic import Sanic, response


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
        data = {'user_id': user_id, 'funds': float(amount)}
        result, status = await self.postRequest(self.cacheURL+"/funds/add_funds", data)
        return result, status

    async def getQuote(self, trans_num, user_id, stock_id):
        result, status = await self.getRequest(self.cacheURL + f"/quote/get/{user_id}/{stock_id}/{trans_num}")
        return result, status

    async def buyStock(self, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status == 200:
            quotePrice = float(result['content']['price'])
            if float(quotePrice) > float(amount):
                return errorResult(err="Not enough capital to buy this stock.", data=''), 400
            totalStock = floor(float(amount)/float(quotePrice))
            totalValue = round(quotePrice*totalStock, 2)
            result, status = await self.getRequest(self.cacheURL + f"/funds/get/user/{user_id}")
            if status == 200:
                userBal = result['content']
                if totalValue > float(userBal):
                    return errorResult(err="User doesn't have required funds", data=''), 400
                data = {'user_id': user_id, 'stock_symbol': stock_symbol, 'stock_amount': totalStock, 'funds': totalValue}
                result, status = await self.postRequest(self.cacheURL+"/stocks/buy_stocks", data)
                return result, status
            else:
                return result, status
        else:
            return result, status

    async def getBuy(self, user_id):
        result, status = await self.getRequest(self.cacheURL + f"/stocks/get_buy/{user_id}")
        return result, status

    async def commitBuy(self, trans_num, user_id):
        result, status = await self.getBuy(user_id)
        if status == 200:
            check = result['content']
            data = {'user_id': user_id}
            then = float(check['time'])
            now = currentTime()
            difference = (now-then)
            if difference < 60:
                result, status = await self.postRequest(self.cacheURL + "/stocks/commit_buy", data)
                return result, status
            else:
                return errorResult(err="Previous buy has expired", data=''), 400
        else:
            return result, status

    async def cancelBuy(self, trans_num, user_id):
        data = {'user_id': user_id}
        result, status = await self.postRequest(self.cacheURL + "/stocks/cancel_buy", data)
        return result, status

    async def sellStock(self, trans_num, user_id, stock_symbol, amount):
        result, status = await self.getQuote(trans_num, user_id, stock_symbol)
        if status == 200:
            quotePrice = float(result['content']['price'])
            totalStock = ceil(float(amount) / float(quotePrice))
            totalValue = round(quotePrice * totalStock, 2)
            result, status = await self.getRequest(self.cacheURL + f"/stocks/get/user/{user_id}/{stock_symbol}")
            if status == 200:
                stockBal = result['content']
                if totalValue > stockBal:
                    return errorResult(err="User doesn't have required stocks", data=''), 400
                data = {'user_id': user_id, 'stock_symbol': stock_symbol, 'stock_amount': totalStock,
                        'funds': totalValue}
                result, status = await self.postRequest(self.cacheURL + "/stocks/sell_stocks", data)
                return result, status
            else:
                return result, status
        else:
            return result, status

    async def getSell(self, user_id):
        result, status = await self.getRequest(self.cacheURL + f"/stocks/get_sell/{user_id}")
        return result, status

    async def commitSell(self, trans_num, user_id):
        result, status = await self.getSell(user_id)
        if status == 200:
            check = result['content']
            data = {'user_id': user_id}
            then = float(check['time'])
            now = currentTime()
            difference = (now - then)
            if difference < 60:
                result, status = await self.postRequest(self.cacheURL + "/stocks/commit_sell", data)
                return result, status
            else:
                return errorResult(err="Previous sell has expired", data=''), 400
        else:
            return result, status

    async def cancelSell(self, trans_num, user_id):
        data = {'user_id': user_id}
        result, status = await self.postRequest(self.cacheURL + "/stocks/cancel_sell", data)
        return result, status

    # __________________________________________________________________________________________________________________

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            status = resp.status
            return js, status

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            status = resp.status
            return js, status
