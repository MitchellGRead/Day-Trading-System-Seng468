class ServiceLogic:

    def __init__(self, BaseLogic, LegacyStockServerHandler):
        self.BaseLogic = BaseLogic
        self.LegacyStockServerHandler = LegacyStockServerHandler

    def addFunds(self, trans_num, user_id, amount):
        result = await self.BaseLogic.addFunds(trans_num, user_id, amount)
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
