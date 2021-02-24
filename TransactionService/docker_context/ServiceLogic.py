class ServiceLogic:

    def __init__(self, TransactionHandler):
        self.TransactionHandler = TransactionHandler

    def addFunds(self, trans_num, user_id, amount):
        result = await self.TransactionHandler.addFunds(trans_num, user_id, amount)
        return result

    def getQuote(self, trans_num, user_id, stock_id):
        result = await self.TransactionHandler.getQuote(trans_num, user_id, stock_id)
        return result

    def buyStock(self, trans_num, user_id, stock_symbol, amount):
        result = await self.TransactionHandler.buyStock(trans_num, user_id, stock_symbol, amount)
        return result

    def commitBuy(self, trans_num, user_id):
        result = await self.TransactionHandler.commitBuy(trans_num, user_id)
        return result

    def cancelBuy(self, trans_num, user_id):
        result = await self.TransactionHandler.cancelBuy(trans_num, user_id)
        return result

    def sellStock(self, trans_num, user_id, stock_symbol, amount):
        result = await self.TransactionHandler.sellStock(trans_num, user_id, stock_symbol, amount)
        return result

    def commitSell(self, trans_num, user_id):
        result = await self.TransactionHandler.commitSell(trans_num, user_id)
        return result

    def cancelSell(self, trans_num, user_id):
        result = await self.TransactionHandler.cancelSell(trans_num, user_id)
        return result
