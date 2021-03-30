from Client import Client


class TransactionHandler:

    def __init__(self, cache_ip, cache_port, trigger_ip, trigger_port, loop):
        self.url = f'http://{cache_ip}:{cache_port}'
        self.triggerURL = f'http://{trigger_ip}:{trigger_port}'
        self.client = Client(loop)

    async def handleQuote(self, data):
        endpoint = f'/quote/get/{data["user_id"]}/{data["stock_symbol"]}/{data["transaction_num"]}'
        resp, status = await self.client.getRequest(f'{self.url}{endpoint}')
        return resp, status

    async def handleAdd(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/funds/add_funds', data)
        return resp, status

    async def handleBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/stocks/buy_stocks', data)
        return resp, status

    async def handleCommitBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/stocks/commit_buy', data)
        return resp, status

    async def handleCancelBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/stocks/cancel_buy', data)
        return resp, status

    async def handleSell(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/stocks/sell_stocks', data)
        return resp, status

    async def handleCommitSell(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/stocks/commit_sell', data)
        return resp, status

    async def handleCancelSell(self, data):
        resp = await self.client.postRequest(f'{self.url}/stocks/cancel_sell', data)
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
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/sell/amount', data)
        return resp

    async def handleSellTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/sell/set', data)
        return resp

    async def handleCancelSellTrigger(self, data):
        resp = await self.client.postRequest(f'{self.triggerURL}/trigger/sell/cancel', data)
        return resp
