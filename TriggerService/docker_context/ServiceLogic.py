from sanic.log import logger


class ServiceLogic:

    def __init__(self, trigger_handler, trigger_execution):
        self.trigger_handler = trigger_handler
        self.trigger_execution = trigger_execution

    # Only run on startup
    async def initActiveTriggers(self):
        # triggers = await self.trigger_handler.fetchExistingTriggers()
        # self.trigger_execution.addTriggers(triggers)
        pass

    async def setBuyAmount(self, data):
        return await self.trigger_handler.setBuyAmount(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

    async def setBuyTrigger(self, data):
        return await self.trigger_handler.setBuyTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

    async def cancelBuyTrigger(self, data):
        return await self.trigger_handler.cancelBuyTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol']
        )

    async def setSellAmount(self, data):
        return await self.trigger_handler.setSellAmount(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

    async def setSellTrigger(self, data):
        return await self.trigger_handler.setSellTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

    async def cancelSellTrigger(self, data):
        return await self.trigger_handler.cancelSellTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol']
        )
