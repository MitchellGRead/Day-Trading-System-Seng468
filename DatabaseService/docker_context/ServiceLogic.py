
class ServiceLogic:

    def __init__(self, postgresHandler, mongoHandler):
        self.psqlHandler = postgresHandler
        self.mongoHandler = mongoHandler

    async def handleGetAllFundsCommand(self):
        result, status = await self.psqlHandler.handleGetAllFundsCommand()
        return result, status

    async def handleGetFundsCommand(self, user_id):    
        result, status = await self.psqlHandler.handleGetUserFundsCommand(user_id)
        return result, status

    async def handleGetAllStocksCommand(self):
        result, status = await self.psqlHandler.handleGetAllStocksCommand()
        return result, status

    async def handleGetStocksCommand(self, user_id, stock_id):
        result, status = await self.psqlHandler.handleGetUserStocksCommand(user_id, stock_id)
        return result, status

    async def handleGetAllTriggers(self):
        result = await self.psqlHandler.handleGetAllTriggers()
        return result

    async def handleGetAllBuyTriggers(self):
        result = await self.psqlHandler.handleGetAllBuyTriggers()
        return result

    async def handleGetUserBuyTriggers(self, user_id):
        result = await self.psqlHandler.handleGetUserBuyTriggers(user_id)
        return result

    async def handleGetAllSellTriggers(self):
        result = await self.psqlHandler.handleGetAllSellTriggers()
        return result

    async def handleGetUserSellTriggers(self, user_id):
        result = await self.psqlHandler.handleGetUserSellTriggers(user_id)
        return result

    async def handleGetSummaryCommand(self, user_id):
        result = await self.psqlHandler.handleGetSummary(user_id)
        return result
    
    async def handleGetDumplogCommand(self, user_id):
        result = await self.mongoHandler.handleGetDumplogCommand(user_id)
        return result

    async def handleAddFundsCommand(self, user_id, funds):
        result, status = await self.psqlHandler.handleAddFundsCommand(user_id, funds)
        return result, status

    async def handleBuyStocksCommand(self, user_id, stock_id, stock_num, funds):
        result, status = await self.psqlHandler.handleBuyStocksCommand(user_id, stock_id, stock_num, funds)
        return result, status

    async def handleSellStocksCommand(self, user_id, stock_id, stock_num, funds):
        result, status = await self.psqlHandler.handleSellStocksCommand(user_id, stock_id, stock_num, funds)
        return result, status

    async def handleBuyTriggerAmount(self, user_id, stock_id, amount):
        result = await self.psqlHandler.handleBuyTriggerAmount(user_id, stock_id, amount)
        return result
    
    async def handleBuyTriggerPrice(self, user_id, stock_id, price, transaction_num):
        result = await self.psqlHandler.handleBuyTriggerPrice(user_id, stock_id, price, transaction_num)
        return result
    
    async def handleExecuteBuyTrigger(self, user_id, stock_id, funds):
        result = await self.psqlHandler.handleExecuteBuyTrigger(user_id, stock_id, funds)
        return result

    async def handleCancelBuyTrigger(self, user_id, stock_id):
        result = await self.psqlHandler.handleCancelBuyTrigger(user_id, stock_id)
        return result

    async def handleSellTriggerAmount(self, user_id, stock_id, amount):
        result = await self.psqlHandler.handleSellTriggerAmount(user_id, stock_id, amount)
        return result
    
    async def handleSellTriggerPrice(self, user_id, stock_id, price, transaction_num):
        result = await self.psqlHandler.handleSellTriggerPrice(user_id, stock_id, price, transaction_num)
        return result

    async def handleExecuteSellTrigger(self, user_id, stock_id, funds):
        result = await self.psqlHandler.handleExecuteSellTrigger(user_id, stock_id, funds)
        return result

    async def handleCancelSellTrigger(self, user_id, stock_id):
        result = await self.psqlHandler.handleCancelSellTrigger(user_id, stock_id)
        return result

    async def handleAddUserAuditEvent(self, user_id, audit_data):
        result = await self.mongoHandler.handleAddUserAuditEvent(user_id, audit_data)
        return result
    
    async def handleAddSystemAuditEvent(self, audit_data):
        result = await self.mongoHandler.handleAddSystemAuditEvent(audit_data)
        return result
