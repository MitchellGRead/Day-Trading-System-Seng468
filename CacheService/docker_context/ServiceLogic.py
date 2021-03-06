class ServiceLogic:

    def __init__(self, CacheLogic):
        self.CacheLogic = CacheLogic

    async def getUserFunds(self, user_id):
        return await self.CacheLogic.getUserFunds(user_id)

    async def getUserStocks(self, user_id, stock_id):
        return await self.CacheLogic.getUserStocks(user_id, stock_id)

    async def addFunds(self, data):
        return await self.CacheLogic.addFunds(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            funds=data['amount']
        )

    async def buyStocks(self, data):
        return await self.CacheLogic.buyStocks(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount']
        )

    async def sellStocks(self, data):
        return await self.CacheLogic.sellStocks(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount']
        )

    async def getBuyStocks(self, user_id):
        return await self.CacheLogic.getBuyStocks(user_id)

    async def getSellStocks(self, user_id):
        return await self.CacheLogic.getSellStocks(user_id)

    async def commitBuyStocks(self, data):
        return await self.CacheLogic.commitBuyStocks(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def commitSellStocks(self, data):
        return await self.CacheLogic.commitSellStocks(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def cancelBuy(self, data):
        return await self.CacheLogic.cancelBuy(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def cancelSell(self, data):
        return await self.CacheLogic.cancelSell(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def getQuote(self, trans_num, user_id, stock_id):
        return await self.CacheLogic.getQuote(trans_num, user_id, stock_id)

    async def getBulkQuote(self, user_ids, stock_ids, transaction_nums):
        return await self.CacheLogic.getBulkQuote(user_ids, stock_ids, transaction_nums)

    async def updateUserCache(self, user_id):
        await self.CacheLogic.cacheAccountTransaction(user_id)
        return {'message': "update processed", 'content': ''}, 200

    async def updateStockCache(self, user_id, stock_id):
        await self.CacheLogic.cacheStockTransaction(user_id, stock_id)
        return {'message': "update processed", 'content': ''}, 200
