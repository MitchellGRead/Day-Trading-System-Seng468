from sanic import response
from time import time


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

    def __init__(self, redis, RedisHandler, audit, client, ip, port, LegacyStock):
        self.LegacyStock = LegacyStock
        self.redis = redis
        self.RedisHandler = RedisHandler
        self.audit = audit
        self.client = client
        self.dbmURL = f'http://{ip}:{port}'

    async def getUserFunds(self, user_id):
        result = await self.RedisHandler.rExists(user_id)
        if result:
            data = await self.RedisHandler.rGet(user_id)
            return goodResult(msg="User Data", data=data['account_balance']), 200
        else:
            result, status = await self.RedisHandler.updateAccountCache(user_id)
            if status == 200:
                data = await self.RedisHandler.rGet(user_id)
                return goodResult(msg="User Data", data=data['account_balance']), 200
            else:
                return result, status

    async def getUserStocks(self, user_id, stock_id):
        check = await self.RedisHandler.rExists(user_id + "_" + stock_id)
        if check:
            data = await self.RedisHandler.rGet(user_id + "_" + stock_id)
            return goodResult(msg="Stock Data", data=data['stock_amount']), 200
        else:
            stockResult, stockStatus = await self.RedisHandler.updateStockCache(user_id, stock_id)
            if stockStatus == 200:
                data = await self.RedisHandler.rGet(user_id + "_" + stock_id)
                return goodResult(msg="Stock Data", data=data['stock_amount']), 200
            else:
                return stockResult, stockStatus

    async def addFunds(self, user_id, funds):
        data = {"user_id": user_id, "funds": float(funds)}
        result, status = await self.postRequest(self.dbmURL + "/funds/add_funds", data)
        if status == 200:
            loop = 0
            while loop < 5:
                accountResult, accountStatus = await self.RedisHandler.updateAccountCache(user_id)
                if accountStatus == 200:
                    break
                loop += 1
        return result, status

    async def buyStocks(self, user_id, stock_symbol, stock_amount, totalValue):
        data = {"user_id": user_id, "stock_id": stock_symbol, "amount": totalValue,
                "amount_of_stock": stock_amount, "time": currentTime()}
        await self.RedisHandler.rSet(user_id + "_BUY", data)
        return goodResult(msg="Buy created", data=''), 200

    async def sellStocks(self, user_id, stock_symbol, amountOfStock, totalValue):
        data = {"user_id": user_id, "stock_id": stock_symbol,
                "amount": totalValue, "amount_of_stock": amountOfStock, "time": currentTime()}
        await self.RedisHandler.rSet(user_id + "_SELL", data)
        return goodResult(msg="Sell created", data=''), 200

    async def getBuyStocks(self, user_id):
        check = await self.RedisHandler.rExists(user_id + "_BUY")
        if check:
            return goodResult(msg="Return buy stock", data=await self.RedisHandler.rGet(user_id + "_BUY")), 200
        else:
            return errorResult(err="Buy doesn't exist", data=''), 404

    async def getSellStocks(self, user_id):
        check = await self.RedisHandler.rExists(user_id + "_SELL")
        if check:
            return goodResult(msg="Return sell stock", data=await self.RedisHandler.rGet(user_id + "_SELL")), 200
        else:
            return errorResult(err="Sell doesn't exist", data=''), 404

    async def commitBuyStocks(self, user_id):
        buy_request = await self.RedisHandler.rGet(user_id + "_BUY")
        data = {"user_id": user_id, "funds": buy_request['amount'],
                "stock_symbol": buy_request['stock_id'], "stock_amount": buy_request['amount_of_stock']}
        result, status = await self.postRequest(self.dbmURL + '/stocks/buy_stocks', data)
        if status == 200:
            loop = 0
            while loop < 5:
                accountResult, accountStatus = await self.RedisHandler.updateAccountCache(user_id)
                stockResult, stockStatus = await self.RedisHandler.updateStockCache(user_id, buy_request['stock_id'])
                if accountStatus == 200 and stockStatus == 200:
                    break
                loop += 1
        await self.RedisHandler.rDelete(user_id + "_BUY")
        return result, status

    async def commitSellStocks(self, user_id):
        sell_request = await self.RedisHandler.rGet(user_id + "_SELL")
        data = {"user_id": user_id, "funds": sell_request["amount"],
                "stock_symbol": sell_request["stock_id"], "stock_amount": sell_request["amount_of_stock"]}
        result, status = await self.postRequest(self.dbmURL + '/stocks/sell_stocks', data)
        if status == 200:
            loop = 0
            while loop < 5:
                accountResult, accountStatus = await self.RedisHandler.updateAccountCache(user_id)
                stockResult, stockStatus = await self.RedisHandler.updateStockCache(user_id, sell_request['stock_id'])
                if accountStatus == 200 and stockStatus == 200:
                    break
                loop += 1
        await self.RedisHandler.rDelete(user_id + "_BUY")
        return result, status

    async def cancelBuy(self, user_id):
        result = await self.RedisHandler.rExists(user_id + "_BUY")
        if result:
            await self.RedisHandler.rDelete(user_id + "_BUY")
            return goodResult(msg="Buy Cancelled", data=''), 200
        else:
            return errorResult(err="No buy request exists", data=''), 404

    async def cancelSell(self, user_id):
        result = await self.RedisHandler.rExists(user_id + "_SELL")
        if result:
            await self.RedisHandler.rDelete(user_id + "_SELL")
            return goodResult(msg="Sell Cancelled", data=''), 200
        else:
            return errorResult(err="No sell request exists", data=''), 404

    async def getQuote(self, trans_num, user_id, stock_id):
        check = await self.RedisHandler.rExists(stock_id)
        if check:
            quote = await self.RedisHandler.rGet(stock_id)
            then = float(quote['time'])
            now = currentTime()
            difference = (now - then)
            if difference < 10:
                return goodResult(msg="Quote price", data={'price': quote['price']}), 200

        result, status = await self.LegacyStock.getQuote(trans_num, user_id, stock_id)
        if status == 200:
            await self.RedisHandler.rSet(stock_id, {'stock_id': stock_id, 'price': result['price'], 'time': currentTime()})
            return goodResult(msg="Quote price", data=result), 200
        else:
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
