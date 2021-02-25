import pickle
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


class RedisHandler:

    def __init__(self, redis, client, ip, port):
        self.redis = redis
        self.client = client
        self.url = f"http://{ip}:{port}"

    async def fillUserCache(self):
        results = await self.getRequest(self.url + '/funds/get/all')
        if results.status == 200:
            data = results.json
            for key in data:
                user_id = key
                userData = results[key]
                user = {"user_id": user_id, "account_balance": userData['available_funds'],
                        "reserved_balance": userData['reserved_funds']}
                self.redis.set(user_id, pickle.dumps(user))
            return response.json(goodResult(msg="Pulled Data", data=''), status=200)
        else:
            return results

    async def fillStockCache(self):
        results = await self.getRequest(self.url + '/stocks/get/all')
        if results.status == 200:
            data = results.json
            for user_id in data:
                usersData = data[user_id]
                for dictionary in usersData:
                    for stock in dictionary:
                        stockInfo = dictionary[stock]
                        stockBalance = {"user_id": user_id, "stock_id": stock,
                                        "stock_amount": stockInfo[0], "stock_reserved": stockInfo[1]}
                        self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stockBalance))
            return response.json(goodResult(msg="Pulled Data", data=''), status=200)
        else:
            return results

    async def updateAccountCache(self, user_id):
        results = await self.getRequest(self.url + '/funds/get/user/' + user_id)
        if results.status == 200:
            data = results.json
            user = {"user_id": user_id, "account_balance": data['available_funds'],
                    "reserved_balance": data['reserved_funds']}
            self.redis.set(user_id, pickle.dumps(user))
            return response.json(goodResult(msg="Pulled Data", data=''), status=200)
        else:
            return results

    async def updateStockCache(self, user_id, stock_symbol):
        results = await self.getRequest(self.url + '/stocks/get/user/' + user_id + "?stock_id=" + stock_symbol)
        if results.status == 200:
            data = results.json
            for stock in data:
                stockInfo = data[stock]
                stockBalance = {"user_id": user_id, "stock_id": stock, "stock_amount":
                                stockInfo['stock_available'], "stock_reserved": stockInfo['stock_reserved']}
                self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stockBalance))
            return response.json(goodResult(msg="Pulled Data", data=''), status=200)
        else:
            return results

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
