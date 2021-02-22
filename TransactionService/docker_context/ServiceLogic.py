class ServiceLogic:

    def __init__(self, BaseLogic, RedisHandler, LegacyStockServerHandler):
        self.BaseLogic = BaseLogic
        self.RedisHandler = RedisHandler
        self.LegacyStockServerHandler = LegacyStockServerHandler
        await self.RedisHandler.fillCache()

    def addFunds(self, trans_num, user_id, amount):
        result = await self.BaseLogic.addFunds(trans_num, user_id, amount)
        await self.RedisHandler.updateAccountCache(user_id)
        return result

    def getQuote(self, trans_num, user_id, stock_id):
        result = await self.BaseLogic.getQuote(trans_num, user_id, stock_id)
        return result

    def buyStock(self, trans_num, user_id, stock_symbol, amount):
        result = await self.BaseLogic.buyStock(trans_num, user_id, stock_symbol, amount)
        return result

    def commitBuy(self, trans_num, user_id):
        result = await self.BaseLogic.commitBuy(trans_num, user_id)
        return result

    def cancelBuy(self, trans_num, user_id):
        result = await self.BaseLogic.cancelBuy(trans_num, user_id)
        return result

    def sellStock(self, trans_num, user_id, stock_symbol, amount):
        result = await self.BaseLogic.sellStock(trans_num, user_id, stock_symbol, amount)
        return result

    def commitSell(self, trans_num, user_id):
        result = await self.BaseLogic.commitSell(trans_num, user_id)
        return result

    def cancelSell(self, trans_num, user_id):
        result = await self.BaseLogic.cancelSell(trans_num, user_id)
        return result
