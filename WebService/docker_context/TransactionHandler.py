from Client import Client


class TransactionHandler:

    def __init__(self, ip, port, loop):
        self.url = f'http://{ip}:{port}'
        self.client = Client(loop)

    async def handleQuote(self, data):
        endpoint = f'/get/{data["command"]}/trans/{data["transaction_num"]}/user/{data["user_id"]}/stock/{data["stock_symbol"]}'
        resp, status = await self.client.getRequest(f'{self.url}{endpoint}')
        return resp, status

    async def handleAdd(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/add', data)
        return resp, status

    async def handleBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/buy', data)
        return resp, status

    async def handleCommitBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/buy/commit', data)
        return resp, status

    async def handleCancelBuy(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/buy/cancel', data)
        return resp, status

    async def handleSell(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/sell', data)
        return resp, status

    async def handleCommitSell(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/sell/commit', data)
        return resp, status

    async def handleCancelSell(self, data):
        resp, status = await self.client.postRequest(f'{self.url}/sell/cancel', data)
        return resp, status
