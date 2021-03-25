from Client import Client


class TransactionHandler:

    def __init__(self, transaction_ip, transaction_port, trigger_ip, trigger_port, loop):
        self.url = f'http://{transaction_ip}:{transaction_port}'
        self.triggerURL = f'http://{trigger_ip}:{trigger_port}'
        self.client = Client(loop)

    async def handleQuote(self, data):
        endpoint = f'/get/{data["command"]}/trans/{data["transaction_num"]}/user/{data["user_id"]}/stock/{data["stock_symbol"]}'
        resp = await self.client.getRequest(f'{self.url}{endpoint}')
        return resp

    async def handleAdd(self, data):
        resp = await self.client.postRequest(f'{self.url}/add', data)
        return resp

    async def handleBuy(self, data):
        resp = await self.client.postRequest(f'{self.url}/buy', data)
        return resp

    async def handleCommitBuy(self, data):
        resp = await self.client.postRequest(f'{self.url}/buy/commit', data)
        return resp

    async def handleCancelBuy(self, data):
        resp = await self.client.postRequest(f'{self.url}/buy/cancel', data)
        return resp

    async def handleSell(self, data):
        resp = await self.client.postRequest(f'{self.url}/sell', data)
        return resp

    async def handleCommitSell(self, data):
        resp = await self.client.postRequest(f'{self.url}/sell/commit', data)
        return resp

    async def handleCancelSell(self, data):
        resp = await self.client.postRequest(f'{self.url}/sell/cancel', data)
        return resp

    async def handleBuyAmount(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/amount', data)
        return resp

    async def handleBuyTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/set', data)
        return resp

    async def handleCancelBuyTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/cancel', data)
        return resp

    async def handleSellAmount(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/amount', data)
        return resp

    async def handleSellTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/set', data)
        return resp

    async def handleCancelSellTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/buy/cancel', data)
        return resp
