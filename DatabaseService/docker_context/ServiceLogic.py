#TODO: Return response code along with data

class ServiceLogic:

    def __init__(self, postgresHandler):
        self.psqlHandler = postgresHandler

    async def handleGetAllFundsCommand(self):
        result = await self.psqlHandler.handleGetAllFundsCommand()
        return result

    async def handleGetFundsCommand(self, user_id):    
        result = await self.psqlHandler.handleGetUserFundsCommand(user_id)
        return result

    async def handleGetAllStocksCommand(self):
        result = await self.psqlHandler.handleGetAllStocksCommand()
        return result

    async def handleGetStocksCommand(self, user_id, stock_id):
        result = await self.psqlHandler.handleGetUserStocksCommand(user_id, stock_id)
        return result
    
    async def handleGetSummaryCommand(self, user_id):
        # TODO: Talk to both Postgres and Mongo to get the required data
        return None

    async def handleAddFundsCommand(self, user_id, funds):
        result = await self.psqlHandler.handleAddFundsCommand(user_id, funds)
        return result

    async def handleBuyStocksCommand(self, user_id, stock_id, stock_num, funds):
        result = await self.psqlHandler.handleBuyStocksCommand(user_id, stock_id, stock_num, funds)
        return result

    async def handleSellStocksCommand(self, user_id, stock_id, stock_num, funds):
        result = await self.psqlHandler.handleSellStocksCommand(user_id, stock_id, stock_num, funds)
        return result