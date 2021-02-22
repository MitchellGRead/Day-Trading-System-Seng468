import pickle
from datetime import datetime

class TransactionHandler:

    def __init__(self, LegacyStockServerHandler, redis, RedisHandler, audit, client, ip, port):
        self.LegacyStockServer = LegacyStockServerHandler
        self.redis = redis
        self.RedisHandler = RedisHandler
        self.audit = audit
        self.client = client
        self.dbmURL = f'http://{ip}:{port}'

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js

    async def addFunds(self, trans_num, user_id, amount):
        data = {'user_id': user_id, 'funds': float(amount)}
        result = await self.postRequest(self.dbmURL+"/funds/add_funds", data)
        return result

    async def getQuote(self, trans_num, user_id, stock_id):
        result = await self.LegacyStockServer.getQuote(trans_num, user_id, stock_id)
        return result

    async def buyStock(self, trans_num, user_id, stock_symbol, amount):
        if self.redis.exists(user_id):
            user = pickle.loads(self.redis.get(user_id))
            price = float(await self.LegacyStockServer.getQuote(trans_num, user_id, stock_symbol))
            amountStock = float(amount)/price
            totalValue = amountStock*price
            if float(user["account_balance"]) >= float(amount):
                dictionary = {"user_id": user_id, "stock_id": stock_symbol, "amount": totalValue,
                              "amount_of_stock": amountStock, "time": datetime.now()}
                self.redis.set(user_id + "_BUY", pickle.dumps(dictionary))
                return {"statusMessage": "Buy Created"}
            else:
                return {'errorMessage': 'Specified user does not have sufficient funds'}
        else:
            return {'errorMessage': 'Specified user does not exist'}

    async def commitBuy(self, trans_num, user_id):
        if self.redis.exists(user_id + "_BUY"):
            buyObj = pickle.loads(self.redis.get(user_id + "_BUY"))
            now = datetime.now()
            timeDiff = (now - buyObj["time"]).total_seconds()
            if timeDiff <= 60:
                data = {"user_id": user_id, "funds": buyObj["amount"],
                        "stock_symbol": buyObj["stock_id"], "stock_amount": buyObj["amount_of_stock"]}
                result = await self.postRequest(self.dbmURL+'/stocks/buy_stocks', data)
                self.redis.delete(user_id + "_BUY")
                await self.RedisHandler.updateAccountCache(user_id)
                await self.RedisHandler.updateStockCache(user_id, buyObj['stock_id'])
                return result
            else:
                self.redis.delete(user_id + "_BUY")
                return {'errorMessage': 'Buy command was too old'}
        else:
            return {'errorMessage': 'Specified user does not have an existing buy in progress'}

    async def cancelBuy(self, trans_num, user_id):
        if self.redis.exists(user_id + "_BUY"):
            self.redis.delete(user_id + "_BUY")
            return {'statusMessage': 'Buy was cancelled'}
        else:
            return {'errorMessage': 'Specified user does not have an existing buy to cancel'}

    async def sellStock(self, trans_num, user_id, stock_symbol, amount):
        if self.redis.exists(user_id + "_" + stock_symbol):
            user = pickle.loads(self.redis.get(user_id + "_" + stock_symbol))
            price = float(self.LegacyStockServer.quote(trans_num, user_id, stock_symbol))
            amountOfStock = float(amount) / price
            totalValue = float(amount) * price

            if int(user["stock_amount"]) >= amountOfStock:
                dictionary = {"user_id": user_id, "stock_id": stock_symbol,
                              "amount": totalValue, "amount_of_stock": amountOfStock, "time": datetime.now()}
                self.redis.set(user_id + "_SELL", pickle.dumps(dictionary))
                return {"statusMessage": "Sell created"}
            else:
                return {'errorMessage': "User doesn't have the required amount of stock"}
        else:
            return {'errorMessage': 'Specified user does not own that stock'}

    async def commitSell(self, trans_num, user_id):
        if self.redis.exists(user_id + "_SELL"):
            sellObj = pickle.loads(self.redis.get(user_id + "_SELL"))
            now = datetime.now()
            timeDiff = (now - sellObj["time"]).total_seconds()
            if timeDiff <= 60:
                data = {"user_id": user_id, "funds": sellObj["amount"],
                        "stock_symbol": sellObj["stock_id"], "stock_amount": sellObj["amount_of_stock"]}
                result = await self.postRequest(self.dbmURL+'/stocks/sell_stocks', data)

                self.redis.delete(user_id + "_SELL")
                self.RedisHandler.updateAccountCache(user_id)
                self.RedisHandler.updateStockCache(user_id, sellObj["stock_id"])
                return result
            else:
                self.redis.delete(user_id + "_SELL")
                return {'errorMessage': 'sell command was too old'}
        else:
            return {'errorMessage': 'Specified user does not have an existing sell in progress'}

    async def cancelSell(self, trans_num, user_id):
        if self.redis.exists(user_id + "_SELL"):
            self.redis.delete(user_id + "_SELL")
            return {'statusMessage': 'Sell was cancelled'}
        else:
            return {'errorMessage': 'Specified user does not have an existing sell to cancel'}
