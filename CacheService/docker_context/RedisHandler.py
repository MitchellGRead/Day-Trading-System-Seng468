import pickle

import aiohttp
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


class RedisHandler:

    def __init__(self, redis, ip, port, loop):
        self.redis = redis
        self.client = Client(loop)
        self.dbm_url = f"http://{ip}:{port}"

    async def fillUserCache(self):
        data, status = await self.client.getRequest(f'{self.dbm_url}/funds/get/all')
        if status == 200:
            for key in data:
                user_id = key
                user_data = data[key]
                user = {
                    "user_id": user_id,
                    "account_balance": user_data['available_funds'],
                    "reserved_balance": user_data['reserved_funds']
                }
                await self.redis.set(user_id, pickle.dumps(user))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            return data, status

    async def fillStockCache(self):
        data, status = await self.client.getRequest(f'{self.dbm_url}/stocks/get/all')
        if status == 200:
            for user_id in data:
                users_data = data[user_id]
                for dictionary in users_data:
                    for stock in dictionary:
                        stock_info = dictionary[stock]
                        stock_balance = {
                            "user_id": user_id,
                            "stock_id": stock,
                            "stock_amount": stock_info[0],
                            "stock_reserved": stock_info[1]
                        }
                        await self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stock_balance))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            return data, status

    async def updateAccountCache(self, user_id):
        data, status = await self.client.getRequest(f'{self.dbm_url}/funds/get/user/{user_id}')
        if status == 200:
            user = {
                "user_id": user_id,
                "account_balance": data['available_funds'],
                "reserved_balance": data['reserved_funds']
            }
            await self.redis.set(user_id, pickle.dumps(user))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            logger.info(f'{__name__} - Error from DBM to get user when updating account cache - {data} ({status})')
            return data, status

    async def updateStockCache(self, user_id, stock_symbol):
        data, status = await self.client.getRequest(f'{self.dbm_url}/stocks/get/user/{user_id}?stock_id={stock_symbol}')
        if not data:
            err_msg = "The user doesn't hold that stock"
            logger.info(f'{__name__} - {err_msg}')
            return errorResult(err_msg, ''), 404
        if status == 200:
            for stock in data:
                stock_info = data[stock]
                stock_balance = {
                    "user_id": user_id,
                    "stock_id": stock,
                    "stock_amount": stock_info[0],
                    "stock_reserved": stock_info[1]
                }
                await self.redis.set("{}_{}".format(user_id, stock), pickle.dumps(stock_balance))
            return goodResult(msg="Pulled Data", data=''), 200
        else:
            logger.info(f'{__name__} - Error from DBM to getting user stock data - {data} ({status})')
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
