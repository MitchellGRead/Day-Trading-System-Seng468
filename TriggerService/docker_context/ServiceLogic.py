from sanic.log import logger
from TriggerExecutionManager import TriggerExecutionManager


class ServiceLogic:

    def __init__(self, trigger_handler, trigger_execution):
        self.trigger_handler = trigger_handler
        self.trigger_execution = trigger_execution

    # Only run on startup
    async def initActiveTriggers(self):
        triggers = await self.trigger_handler.fetchExistingTriggers()
        self.trigger_execution.addTriggers(triggers)
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
        result, status = await self.trigger_handler.setBuyTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

        if status == 200:
            trigger = result[0]
            replace = result[1]
            if replace:
                toReplace = self.trigger_execution.getTrigger(data['user_id'], data['stock_symbol'],
                                                              TriggerExecutionManager.BUY)
                await self.trigger_execution.updateTrigger(toReplace, trigger)
            else:
                result, status = self.trigger_execution.addTrigger(trigger)
        return result, status

    async def cancelBuyTrigger(self, data):
        trigger = self.trigger_execution.getTrigger(data['user_id'], data['stock_symbol'], TriggerExecutionManager.BUY)

        if trigger:
            self.trigger_execution.removeTrigger(trigger)
            return await self.trigger_handler.cancelBuyTrigger(
                data['transaction_num'],
                data['command'],
                data['user_id'],
                data['stock_symbol']
            )
        else:
            return "Trigger does not exist", 404

    async def setSellAmount(self, data):
        return await self.trigger_handler.setSellAmount(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

    async def setSellTrigger(self, data):
        result, status = await self.trigger_handler.setSellTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol'],
            data['amount']
        )

        if status == 200:
            trigger = result[0]
            replace = result[1]
            if replace:
                toReplace = self.trigger_execution.getTrigger(data['user_id'], data['stock_symbol'],
                                                              TriggerExecutionManager.SELL)
                await self.trigger_execution.updateTrigger(toReplace, trigger)
            else:
                result, status = self.trigger_execution.addTrigger(trigger)
        return result, status

    async def cancelSellTrigger(self, data):
        trigger = self.trigger_execution.getTrigger(data['user_id'], data['stock_symbol'], TriggerExecutionManager.SELL)

        if trigger:
            self.trigger_execution.removeTrigger(trigger)
        else:
            return "Trigger does not exist", 404

        return await self.trigger_handler.cancelSellTrigger(
            data['transaction_num'],
            data['command'],
            data['user_id'],
            data['stock_symbol']
        )
