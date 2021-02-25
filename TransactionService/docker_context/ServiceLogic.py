class ServiceLogic:

    def __init__(self, TransactionHandler):
        self.TransactionHandler = TransactionHandler

    async def addFunds(self, trans_num, user_id, amount):
        return await self.TransactionHandler.addFunds(trans_num, user_id, amount)

    async def getQuote(self, trans_num, user_id, stock_id):
        return await self.TransactionHandler.getQuote(trans_num, user_id, stock_id)

    async def buyStock(self, trans_num, user_id, stock_symbol, amount):
        return await self.TransactionHandler.buyStock(trans_num, user_id, stock_symbol, amount)

    async def commitBuy(self, trans_num, user_id):
        return await self.TransactionHandler.commitBuy(trans_num, user_id)

    async def cancelBuy(self, trans_num, user_id):
        return await self.TransactionHandler.cancelBuy(trans_num, user_id)

    async def sellStock(self, trans_num, user_id, stock_symbol, amount):
        return await self.TransactionHandler.sellStock(trans_num, user_id, stock_symbol, amount)

    async def commitSell(self, trans_num, user_id):
        return await self.TransactionHandler.commitSell(trans_num, user_id)

    async def cancelSell(self, trans_num, user_id):
        return await self.TransactionHandler.cancelSell(trans_num, user_id)
