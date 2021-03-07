class ServiceLogic:

    def __init__(self, CacheLogic):
        self.CacheLogic = CacheLogic

    async def getUserFunds(self, user_id):
        return await self.CacheLogic.getUserFunds(user_id)

    async def getUserStocks(self, user_id, stock_id):
        return await self.CacheLogic.getUserStocks(user_id, stock_id)

    async def addFunds(self, user_id, funds):
        return await self.CacheLogic.addFunds(user_id, funds)

    async def buyStocks(self, user_id, stock_symbol, stock_amount, total_value):
        return await self.CacheLogic.buyStocks(user_id, stock_symbol, stock_amount, total_value)

    async def sellStocks(self, user_id, stock_symbol, amount_of_stock, total_value):
        return await self.CacheLogic.sellStocks(user_id, stock_symbol, amount_of_stock, total_value)

    async def getBuyStocks(self, user_id):
        return await self.CacheLogic.getBuyStocks(user_id)

    async def getSellStocks(self, user_id):
        return await self.CacheLogic.getSellStocks(user_id)

    async def commitBuyStocks(self, user_id):
        return await self.CacheLogic.commitBuyStocks(user_id)

    async def commitSellStocks(self, user_id):
        return await self.CacheLogic.commitSellStocks(user_id)

    async def cancelBuy(self, user_id):
        return await self.CacheLogic.cancelBuy(user_id)

    async def cancelSell(self, user_id):
        return await self.CacheLogic.cancelSell(user_id)

    async def getQuote(self, trans_num, user_id, stock_id):
        return await self.CacheLogic.getQuote(trans_num, user_id, stock_id)
