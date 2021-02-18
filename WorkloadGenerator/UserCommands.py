
class UserCommands:
    def __init__(self, ip, port, client):
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}'
        self.client = client

    async def getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js

    async def quoteRequest(self, params):
        trans_num, _, user_id, stock_symbol = params
        url = f'{self.url}/quote/trans/{trans_num}/user/{user_id}/stock/{stock_symbol}'

        result = await self.getRequest(url)
        return result

    async def displaySummary(self, params):
        trans_num, _, user_id = params
        url = f'{self.url}/display_summary/trans/{trans_num}/user/{user_id}'

        result = await self.getRequest(url)
        return result

    async def dumplog(self, params):
        request_params = {}
        if len(params) == 3:
            trans_num, _, filename = params
        else:
            trans_num, _, user_id, filename = params
            request_params['user_id'] = user_id

        url = f'{self.url}/dumplog/trans/{trans_num}/file/{filename}'

        result = await self.getRequest(url, request_params)
        return result

    async def addFundsRequest(self, params):
        trans_num, _, user_id, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'amount': float(amount)
        }
        url = f'{self.url}/add'

        result = await self.postRequest(url, data)
        return result

    # BUY REQUESTS --------------------------------------------
    async def buyRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/buy'

        result = await self.postRequest(url, data)
        return result

    def commitBuyRequest(self, params):
        trans_num, _, user_id = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id
        }
        url = f'{self.url}/commit_buy'

        result = self.postRequest(url, data)
        return result


    def cancelBuyRequest(self, params):
        trans_num, _, user_id = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id
        }
        url = f'{self.url}/cancel_buy'

        result = self.postRequest(url, data)
        return result


    def setBuyAmountRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_buy_amount'

        result = self.postRequest(url, data)
        return result

    def setBuyTriggerRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_buy_trigger'

        result = self.postRequest(url, data)
        return result

    def cancelSetBuyRequest(self, params):
        trans_num, _, user_id, stock_symbol = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        url = f'{self.url}/cancel_set_buy'

        result = self.postRequest(url, data)
        return result

    # --------------------------------------------------------------

    # SELL REQUESTS --------------------------------------------
    def sellRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/sell'

        result = self.postRequest(url, data)
        return result

    def commitSellRequest(self, params):
        trans_num, _, user_id = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id
        }
        url = f'{self.url}/commit_sell'

        result = self.postRequest(url, data)
        return result

    def cancelSellRequest(self, params):
        trans_num, _, user_id = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id
        }
        url = f'{self.url}/cancel_sell'

        result = self.postRequest(url, data)
        return result

    def setSellAmountRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_sell_amount'

        result = self.postRequest(url, data)
        return result

    def setSellTriggerRequest(self, params):
        trans_num, _, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_sell_trigger'

        result = self.postRequest(url, data)
        return result

    def cancelSetSellRequest(self, params):
        trans_num, _, user_id, stock_symbol = params
        data = {
            'transaction_num': trans_num,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        url = f'{self.url}/cancel_set_sell'

        result = self.postRequest(url, data)
        return result
    # --------------------------------------------------------------
