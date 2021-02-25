from datetime import datetime
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
        result = await self.postRequest(self.cacheURL+"/funds/add_funds", data)
        return result

    async def getQuote(self, trans_num, user_id, stock_id):
        result = await self.getRequest(self.cacheURL + f"/quote/get/{user_id}/{stock_id}/{trans_num}")
        # DO AUDIT IN CACHE SERVICE
        return result

    async def buyStock(self, trans_num, user_id, stock_symbol, amount):
        quotePrice = await self.getQuote(trans_num, user_id, stock_symbol)
        totalStock = floor(float(amount)/float(quotePrice))
        totalValue = quotePrice*totalStock
        userBal = await self.getRequest(self.cacheURL + f"/funds/get/user/{user_id}")
        userBal = userBal.data
        if totalValue > float(userBal):
            return response.json(errorResult(err="User doesn't have required funds", data=''), status=400)
        data = {'user_id': user_id, 'stock_symbol': stock_symbol, 'stock_amount': totalStock, 'funds': totalValue}
        result = await self.postRequest(self.cacheURL+"/stocks/buy_stock", data)
        return result

    async def getBuy(self, user_id):
        result = await self.getRequest(self.cacheURL + f"/stocks/get_buy/{user_id}")
        return result

    async def commitBuy(self, trans_num, user_id):
        check = await self.getBuy(user_id)
        check = check.data
        if check.status == 200:
            data = {'user_id': user_id}
            then = check['time']
            now = datetime.now()
            difference = (now-then).total_seconds()
            if difference < 60:
                result = await self.postRequest(self.cacheURL + "/stocks/commit_buy", data)
                return result
            else:
                return response.json(errorResult(err="Previous buy has expired", data=''), status=400)
        else:
            return check

    async def cancelBuy(self, trans_num, user_id):
        data = {'user_id': user_id}
        result = await self.postRequest(self.cacheURL + "/stocks/cancel_buy", data)
        return result

    async def sellStock(self, trans_num, user_id, stock_symbol, amount):
        quotePrice = await self.getQuote(trans_num, user_id, stock_symbol)
        totalStock = ceil(float(amount) / float(quotePrice))
        totalValue = quotePrice * totalStock
        stockBal = await self.getRequest(self.cacheURL + f"/stocks/get/user/{user_id}/{stock_symbol}")
        stockBal = stockBal.data
        if totalValue > stockBal:
            return response.json(errorResult(err="User doesn't have required stocks", data=''), status=400)
        data = {'user_id': user_id, 'stock_symbol': stock_symbol, 'stock_amount': totalStock, 'funds': totalValue}
        result = await self.postRequest(self.cacheURL + "/stocks/sell_stock", data)
        return result

    async def getSell(self, user_id):
        result = await self.getRequest(self.cacheURL + f"/stocks/get_sell/{user_id}")
        return result

    async def commitSell(self, trans_num, user_id):
        check = await self.getSell(user_id)
        check = check.data
        if check.status == 200:
            data = {'user_id': user_id}
            then = check['time']
            now = datetime.now()
            difference = (now - then).total_seconds()
            if difference < 60:
                result = await self.postRequest(self.cacheURL + "/stocks/commit_sell", data)
                return result
            else:
                return response.json(errorResult(err="Previous sell has expired", data=''), status=400)
        else:
            return check

    async def cancelSell(self, trans_num, user_id):
        data = {'user_id': user_id}
        result = await self.postRequest(self.cacheURL + "/stocks/cancel_sell", data)
        return result

    # __________________________________________________________________________________________________________________

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js
