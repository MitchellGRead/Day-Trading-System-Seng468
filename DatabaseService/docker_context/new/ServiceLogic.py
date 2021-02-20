
class ServiceLogic:

    def __init__(self, postgresHandler):
        self.psqlHandler = postgresHandler

    async def handleGetFundsCommand(self, user_id):    
        result = await self.psqlHandler.handleGetFundsCommand(user_id)
        return result

    async def handleGetStocksCommand(self, user_id, stock_id):
        result = await self.psqlHandler.handleGetStocksCommand(user_id, stock_id)
        return result
    
    async def handleGetSummaryCommand(self, user_id):
        # TODO: Talk to both Postgres and Mongo to get the required data
        return None

    async def handleAddFundsCommand(self, data):
        result = await self.psqlHandler.handleAddFundsCommand(data)
        return result

    async def handleBuyStocksCommand(self, data):
        result = await self.psqlHandler.handleBuyStocksCommand(data)
        return result

    async def handleSellStocksCommand(self, data):
        result = await self.psqlHandler.handleSellStocksCommand(data)
        return result