from datetime import datetime
from sanic import response


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
            return response.json(goodResult(msg="User Data", data=data['account_balance']), status=200)
        else:
            result = await self.RedisHandler.updateAccountCache(user_id)
            if result.status == 200:
                data = await self.RedisHandler.rGet(user_id)
                return response.json(goodResult(msg="User Data", data=data['account_balance']), status=200)
            else:
                return result

    async def getUserStocks(self, user_id, stock_id):
        check = await self.RedisHandler.rExists(user_id + "_" + stock_id)
        if check:
            data = await self.RedisHandler.rGet(user_id + "_" + stock_id)
            return response.json(goodResult(msg="Stock Data", data=data['stock_amount']), status=200)
        else:
            stockResult = await self.RedisHandler.updateStockCache(user_id, stock_id)
            if stockResult.status == 200:
                data = await self.RedisHandler.rGet(user_id + "_" + stock_id)
                return response.json(goodResult(msg="Stock Data", data=data['stock_amount']), status=200)
            else:
                return stockResult

    async def addFunds(self, user_id, funds):
        data = {"user_id": user_id, "funds": float(funds)}
        req, result = await self.postRequest(self.dbmURL + "/funds/add_funds", data)
        if result.status == 200:
            loop = 0
            while loop < 5:
                accountResult = await self.RedisHandler.updateAccountCache(user_id)
                if accountResult.status == 200:
                    break
                loop += 1
        return result

    async def buyStocks(self, user_id, stock_symbol, stock_amount, totalValue):
        data = {"user_id": user_id, "stock_id": stock_symbol, "amount": totalValue,
                "amount_of_stock": stock_amount, "time": datetime.now()}
        self.RedisHandler.rSet(user_id + "_BUY", data)
        return response.json(goodResult(msg="Buy created", data=''), status=200)

    async def sellStocks(self, user_id, stock_symbol, amountOfStock, totalValue):
        data = {"user_id": user_id, "stock_id": stock_symbol,
                "amount": totalValue, "amount_of_stock": amountOfStock, "time": datetime.now()}
        self.RedisHandler.rSet(user_id + "_SELL", data)
        return response.json(goodResult(msg="Sell created", data=''), status=200)

    async def getBuyStocks(self, user_id):
        check = self.RedisHandler.rExists(user_id + "_BUY")
        if check:
            return response.json(goodResult(msg="Return buy stock",
                                            data=await self.RedisHandler.rGet(user_id + "_BUY")), status=200)
        else:
            return response.json(errorResult(err="Buy doesn't exist", data=''), status=404)

    async def getSellStocks(self, user_id):
        check = self.RedisHandler.rExists(user_id + "_SELL")
        if check:
            return response.json(goodResult(msg="Return sell stock",
                                            data=await self.RedisHandler.rGet(user_id + "_SELL")), status=200)
        else:
            return response.json(errorResult(err="Sell doesn't exist", data=''), status=404)

    async def commitBuyStocks(self, user_id):
        buy_request = self.RedisHandler.rGet(user_id + "_BUY")
        data = {"user_id": user_id, "funds": buy_request['amount'],
                "stock_symbol": buy_request['stock_id'], "stock_amount": buy_request['amount_of_stock']}
        result = await self.postRequest(self.dbmURL + '/stocks/buy_stocks', data)
        if result.status == 200:
            loop = 0
            while loop < 5:
                accountResult = await self.RedisHandler.updateAccountCache(user_id)
                stockResult = await self.RedisHandler.updateStockCache(user_id, buy_request['stock_id'])
                if accountResult.status == 200 and stockResult.status == 200:
                    break
                loop += 1
        await self.RedisHandler.rDelete(user_id + "_BUY")
        return result

    async def commitSellStocks(self, user_id):
        sell_request = await self.RedisHandler.rGet(user_id + "_SELL")
        data = {"user_id": user_id, "funds": sell_request["amount"],
                "stock_symbol": sell_request["stock_id"], "stock_amount": sell_request["amount_of_stock"]}
        result = await self.postRequest(self.dbmURL + '/stocks/sell_stocks', data)
        if result.status == 200:
            loop = 0
            while loop < 5:
                accountResult = await self.RedisHandler.updateAccountCache(user_id)
                stockResult = await self.RedisHandler.updateStockCache(user_id, sell_request['stock_id'])
                if accountResult.status == 200 and stockResult.status == 200:
                    break
                loop += 1
        await self.RedisHandler.rDelete(user_id + "_BUY")
        return result

    async def cancelBuy(self, user_id):
        result = self.RedisHandler.rExists(user_id + "_BUY")
        if result:
            self.RedisHandler.rDelete(user_id + "_BUY")
            return response.json(goodResult(msg="Buy Cancelled", data=''), status=200)
        else:
            return response.json(errorResult(err="No buy request exists", data=''), status=404)

    async def cancelSell(self, user_id):
        result = self.RedisHandler.rExists(user_id + "_SELL")
        if result:
            self.RedisHandler.rDelete(user_id + "_SELL")
            return response.json(goodResult(msg="Sell Cancelled", data=''), status=200)
        else:
            return response.json(errorResult(err="No sell request exists", data=''), status=404)

    async def getQuote(self, trans_num, user_id, stock_id):
        check = self.RedisHandler.rExists(stock_id)
        if check:
            quote = self.RedisHandler.rGet(stock_id)
            then = quote['time']
            now = datetime.now()
            difference = (now - then).total_seconds()
            if difference < 10:
                return response.json(goodResult(msg="Quote price", data=quote['price']), status=200)

        result = await self.LegacyStock.getQuote(trans_num, user_id, stock_id)
        self.RedisHandler.rSet(stock_id, {'stock_id': stock_id, 'price': result, 'time': datetime.now()})
        return response.json(goodResult(msg="Quote price", data=result), status=200)

    # __________________________________________________________________________________________________________________

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js
