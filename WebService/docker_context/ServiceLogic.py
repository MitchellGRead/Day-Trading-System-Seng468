import config

class ServiceLogic:

    def __init__(self, client, audit):
        self.client = client
        self.audit = audit
        self.trans_url = f'http://{config.TRANSACTION_SERVER_IP}:{config.TRANSACTION_SERVER_PORT}'

    # HELPER FUNCTIONS -----------------------------------------
    async def __auditTransactionCommand(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount'],
        )

    async def __auditUserCommand(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def __getRequest(self, url, params=None):
        async with self.client.get(url, params=params) as resp:
            js = await resp.json()
            return js

    async def __postRequest(self, url, data):
        async with self.client.post(url, json=data) as resp:
            js = await resp.json()
            return js
    # ----------------------------------------------------------

    async def handleQuote(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol']
        )

        endpoint = f'/quote/trans/{data["transaction_num"]}/user/{data["user_id"]}/stock/{data["stock_symbol"]}'
        resp = await self.__getRequest(f'{self.trans_url}{endpoint}', data)
        return resp

    async def handleDisplaySummary(self, data):
        await self.__auditUserCommand(data)
        # TODO send dumplog command to auditing service as well
        return

    async def handleDumplog(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            filename=data['filename'],
            user_id=data['user_id'] if 'user_id' in data else ''
        )
        # TODO send dumplog command to auditing service as well
        return

    async def handleAdd(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            amount=data['amount'],
        )

        resp = await self.__postRequest(f'{self.trans_url}/add', data)
        return resp

    # BUY COMMAND HANDLING -------------------------------------
    async def handleBuy(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/buy', data)
        return resp

    async def handleCommitBuy(self, data):
        await self.__auditUserCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/buy/commit', data)
        return resp

    async def handleCancelBuy(self, data):
        await self.__auditUserCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/buy/cancel', data)
        return resp
    # ----------------------------------------------------------

    # SELL COMMAND HANDLING -------------------------------------
    async def handleSell(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/sell', data)
        return resp

    async def handleCommitSell(self, data):
        await self.__auditUserCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/sell/commit', data)
        return resp

    async def handleCancelSell(self, data):
        await self.__auditUserCommand(data)
        resp = await self.__postRequest(f'{self.trans_url}/sell/commit', data)
        return resp
    # ----------------------------------------------------------

    # BUY TRIGGER COMMAND HANDLING -----------------------------
    async def handleBuyAmount(self, data):
        await self.__auditTransactionCommand(data)
        # TODO send to trigger service
        return

    async def handleBuyTrigger(self, data):
        await self.__auditUserCommand(data)
        # TODO send to trigger service
        return

    async def handleCancelBuyTrigger(self, data):
        await self.__auditUserCommand(data)
        # TODO send to trigger service
        return
    # ----------------------------------------------------------

    # SELL TRIGGER COMMAND HANDLING ----------------------------
    async def handleSellAmount(self, data):
        await self.__auditTransactionCommand(data)
        # TODO send to trigger service
        return

    async def handleSellTrigger(self, data):
        await self.__auditUserCommand(data)
        # TODO send to trigger service
        return

    async def handleCancelSellTrigger(self, data):
        await self.__auditUserCommand(data)
        # TODO send to trigger service
        return
    # ----------------------------------------------------------
