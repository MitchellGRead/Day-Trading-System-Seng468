from sanic.log import logger


class ServiceLogic:

    def __init__(self, trigger_handler, trigger_execution):
        self.trigger_handler = trigger_handler
        self.trigger_execution = trigger_execution

    # Only run on startup
    async def initActiveTriggers(self):
        triggers = await self.trigger_handler.fetchExistingTriggers()
        self.trigger_execution.addTriggers(triggers)

    async def setBuyAmount(self, data):
        pass

    async def setBuyTrigger(self, data):
        pass

    async def cancelBuyTrigger(self, data):
        pass

    async def setSellAmount(self, data):
        pass

    async def setSellTrigger(self, data):
        pass

    async def cancelSellTrigger(self, data):
        pass