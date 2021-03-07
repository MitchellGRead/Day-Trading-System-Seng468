import pickle

import aiohttp
from sanic import response
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


class RedisHandler:

    def __init__(self, redis, client, ip, port):
        self.redis = redis
        self.client = client
        self.url = f"http://{ip}:{port}"

    async def fillUserCache(self):
        data, status = await self.getRequest(self.url + '/funds/get/all')
        if status == 200:
            for key in data:
                user_id = key
                userData = data[key]
                user = {"user_id": user_id, "account_balance": userData['available_funds'],
                        "reserved_balance": userData['reserved_funds']}
                await self.redis.set(user_id, pickle.dumps(user))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            return data, status

    async def fillStockCache(self):
        data, status = await self.getRequest(self.url + '/stocks/get/all')
        if status == 200:
            for user_id in data:
                usersData = data[user_id]
                for dictionary in usersData:
                    for stock in dictionary:
                        stockInfo = dictionary[stock]
                        stockBalance = {"user_id": user_id, "stock_id": stock,
                                        "stock_amount": stockInfo[0], "stock_reserved": stockInfo[1]}
                        await self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stockBalance))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            return data, status

    async def updateAccountCache(self, user_id):
        data, status = await self.getRequest(self.url + '/funds/get/user/' + user_id)
        if status == 200:
            user = {"user_id": user_id, "account_balance": data['available_funds'],
                    "reserved_balance": data['reserved_funds']}
            await self.redis.set(user_id, pickle.dumps(user))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            # logger.debug(data, status)
            return data, status

    async def updateStockCache(self, user_id, stock_symbol):
        data, status = await self.getRequest(self.url + '/stocks/get/user/' + user_id + "?stock_id=" + stock_symbol)
        if not data:
            return errorResult("The user doesn't hold that stock", ''), 404
        if status == 200:
            for stock in data:
                stockInfo = data[stock]
                stockBalance = {"user_id": user_id, "stock_id": stock, "stock_amount":
                                stockInfo[0], "stock_reserved": stockInfo[1]}
                await self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stockBalance))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            # logger.debug(data, status)
            return data, status

    async def rSet(self, key, values):
        await self.redis.set(key, pickle.dumps(values))
        return

    async def rGet(self, key):
        result = await self.redis.get(key)
        result = pickle.loads(result)
        return result

    async def rExists(self, key):
        result = await self.redis.exists(key)
        return result

    async def rDelete(self, key):
        await self.redis.delete(key)
        return

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
