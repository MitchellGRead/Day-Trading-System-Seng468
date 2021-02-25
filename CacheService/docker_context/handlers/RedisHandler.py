import pickle
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


class RedisHandler:

    def __init__(self, redis, client, ip, port):
        self.redis = redis
        self.client = client
        self.url = f"http://{ip}:{port}"

    async def fillUserCache(self):
        results = await self.getRequest(self.url + '/funds/get/all')
        for row in results:
            user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
            self.redis.set(row[0], pickle.dumps(user))
        return

    async def fillStockCache(self):
        results = await self.getRequest(self.url + '/stocks/get/all')
        for row in results:
            stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
            self.redis.set("{}_{}".format(row[0], row[1]), pickle.dumps(stockBalance))
        return

    async def updateAccountCache(self, user_id):
        results = await self.getRequest(self.url + '/funds/get/user/' + user_id)
        if results.status == 400:
            return results
        for row in results:
            user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
            self.redis.set(row[0], pickle.dumps(user))
        return response.json(goodResult(msg="Pulled Data", data=''), status=200)

    async def updateStockCache(self, user_id, stock_symbol):
        results = await self.getRequest(self.url + '/stocks/get/user/' + user_id + "?stock_id=" + stock_symbol)
        if results.status == 400:
            return results
        for row in results:
            stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
            self.redis.set("{}_{}".format(row[0], row[1]), pickle.dumps(stockBalance))
        return response.json(goodResult(msg="Pulled Data", data=''), status=200)

    async def rSet(self, key, values):
        self.redis.set(key, pickle.dumps(values))
        return

    async def rGet(self, key):
        result = self.redis.get(key)
        result = pickle.loads(result)
        return result

    async def rExists(self, key):
        result = self.redis.exists(key)
        return result

    async def rDelete(self, key):
        self.redis.delete(key)
        return

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js
