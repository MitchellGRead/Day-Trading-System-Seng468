from eventLogger import logger
from time import time


class UserCommands:
    def __init__(self, ip, port, client):
        self.ip = ip
        self.port = port
        self.url = f'http://{self.ip}:{self.port}'
        self.client = client

    async def quoteRequest(self, params):
        trans_num, command, user_id, stock_symbol = params
        url = f'{self.url}/get/{command}/trans/{trans_num}/user/{user_id}/stock/{stock_symbol}'

        result = await self.client.getRequest(url)
        return result

    async def displaySummary(self, params):
        trans_num, command, user_id = params
        url = f'{self.url}/get/{command}/trans/{trans_num}/user/{user_id}'

        result = await self.client.getRequest(url)
        return result

    async def dumplog(self, params):
        request_params = {}
        if len(params) == 3:
            trans_num, command, filename = params
        else:
            trans_num, command, user_id, filename = params
            request_params['user_id'] = user_id

        url = f'{self.url}/get/{command}/trans/{trans_num}/file/{filename}'

        result = await self.client.getRequest(url, request_params)
        return result

    async def addFundsRequest(self, params):
        trans_num, commmand, user_id, amount = params
        data = {
            'transaction_num': trans_num,
            'command': commmand,
            'user_id': user_id,
            'amount': float(amount)
        }
        url = f'{self.url}/add'

        result = await self.client.postRequest(url, data)
        return result

    # BUY REQUESTS --------------------------------------------
    async def buyRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/buy'

        result = await self.client.postRequest(url, data)
        return result

    async def commitBuyRequest(self, params):
        trans_num, command, user_id = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id
        }
        url = f'{self.url}/commit_buy'

        result = await self.client.postRequest(url, data)
        return result

    async def cancelBuyRequest(self, params):
        trans_num, command, user_id = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id
        }
        url = f'{self.url}/cancel_buy'

        result = await self.client.postRequest(url, data)
        return result

    async def setBuyAmountRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_buy_amount'

        result = await self.client.postRequest(url, data)
        return result

    async def setBuyTriggerRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_buy_trigger'

        result = await self.client.postRequest(url, data)
        return result

    async def cancelSetBuyRequest(self, params):
        trans_num, command, user_id, stock_symbol = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        url = f'{self.url}/cancel_set_buy'

        result = await self.client.postRequest(url, data)
        return result

    # --------------------------------------------------------------

    # SELL REQUESTS --------------------------------------------
    async def sellRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/sell'

        result = await self.client.postRequest(url, data)
        return result

    async def commitSellRequest(self, params):
        trans_num, command, user_id = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id
        }
        url = f'{self.url}/commit_sell'

        result = await self.client.postRequest(url, data)
        return result

    async def cancelSellRequest(self, params):
        trans_num, command, user_id = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id
        }
        url = f'{self.url}/cancel_sell'

        result = await self.client.postRequest(url, data)
        return result

    async def setSellAmountRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_sell_amount'

        result = await self.client.postRequest(url, data)
        return result

    async def setSellTriggerRequest(self, params):
        trans_num, command, user_id, stock_symbol, amount = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol,
            'amount': float(amount)
        }
        url = f'{self.url}/set_sell_trigger'

        result = await self.client.postRequest(url, data)
        return result

    async def cancelSetSellRequest(self, params):
        trans_num, command, user_id, stock_symbol = params
        data = {
            'transaction_num': trans_num,
            'command': command,
            'user_id': user_id,
            'stock_symbol': stock_symbol
        }
        url = f'{self.url}/cancel_set_sell'

        result = await self.client.postRequest(url, data)
        return result
    # --------------------------------------------------------------

    async def handleCommand(self, params):
        start_time = time()
        command = params[1]
        if command == 'ADD':
            resp = await self.addFundsRequest(params)
        elif command == 'QUOTE':
            resp = await self.quoteRequest(params)
        elif command == 'BUY':
            resp = await self.buyRequest(params)
        elif command == 'COMMIT_BUY':
            resp = await self.commitBuyRequest(params)
        elif command == 'CANCEL_BUY':
            resp = await self.cancelBuyRequest(params)
        elif command == 'SET_BUY_AMOUNT':
            resp = await self.setBuyAmountRequest(params)
        elif command == 'CANCEL_SET_BUY':
            resp = await self.cancelSetBuyRequest(params)
        elif command == 'SET_BUY_TRIGGER':
            resp = await self.setBuyTriggerRequest(params)
        elif command == 'SELL':
            resp = await self.sellRequest(params)
        elif command == 'COMMIT_SELL':
            resp = await self.commitSellRequest(params)
        elif command == 'CANCEL_SELL':
            resp = await self.cancelSellRequest(params)
        elif command == 'SET_SELL_AMOUNT':
            resp = await self.setSellAmountRequest(params)
        elif command == 'CANCEL_SET_SELL':
            resp = await self.cancelSetSellRequest(params)
        elif command == 'SET_SELL_TRIGGER':
            resp = await self.setSellTriggerRequest(params)
        elif command == 'DISPLAY_SUMMARY':
            resp = await self.displaySummary(params)
        elif command == 'DUMPLOG':
            resp = await self.dumplog(params)
        else:
            logger.warning(f'INVALID COMMAND: {command}')
            return 0

        total_time = time() - start_time
        logger.debug(f'{resp} - {total_time}')
        return total_time
