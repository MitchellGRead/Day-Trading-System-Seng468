class ServiceLogic:

    def __init__(self, transaction_handler):
        self.transaction_handler = transaction_handler

    async def addFunds(self, data):
        return await self.transaction_handler.addFunds(
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            amount=data['amount'],
            command=data['command']
        )

    async def getQuote(self, data):
        return await self.transaction_handler.getQuote(
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol']
        )

    async def buyStock(self, data):
        return await self.transaction_handler.buyStock(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount']
        )

    async def commitBuy(self, data):
        return await self.transaction_handler.commitBuy(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id']
        )

    async def cancelBuy(self, data):
        return await self.transaction_handler.cancelBuy(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id']
        )

    async def sellStock(self, data):
        return await self.transaction_handler.sellStock(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount']
        )

    async def commitSell(self, data):
        return await self.transaction_handler.commitSell(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id']
        )

    async def cancelSell(self, data):
        return await self.transaction_handler.cancelSell(
            command=data['command'],
            trans_num=data['transaction_num'],
            user_id=data['user_id']
        )
