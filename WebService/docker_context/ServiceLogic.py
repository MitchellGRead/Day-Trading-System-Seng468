class ServiceLogic:

    def __init__(self, audit, transaction):
        self.audit = audit
        self.transaction = transaction

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

    # ----------------------------------------------------------

    async def handleQuote(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol']
        )

        resp = await self.transaction.handleQuote(data)
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

        resp = await self.transaction.handleAdd(data)
        return resp

    # BUY COMMAND HANDLING -------------------------------------
    async def handleBuy(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.transaction.handleBuy(data)
        return resp

    async def handleCommitBuy(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCommitBuy(data)
        return resp

    async def handleCancelBuy(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCancelBuy(data)
        return resp
    # ----------------------------------------------------------

    # SELL COMMAND HANDLING -------------------------------------
    async def handleSell(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.transaction.handleSell(data)
        return resp

    async def handleCommitSell(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCommitSell(data)
        return resp

    async def handleCancelSell(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCancelSell(data)
        return resp
    # ----------------------------------------------------------

    # BUY TRIGGER COMMAND HANDLING -----------------------------
    async def handleBuyAmount(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.transaction.handleBuyAmount(data)
        return resp

    async def handleBuyTrigger(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleBuyTrigger(data)
        return resp

    async def handleCancelBuyTrigger(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCancelBuyTrigger(data)
        return resp
    # ----------------------------------------------------------

    # SELL TRIGGER COMMAND HANDLING ----------------------------
    async def handleSellAmount(self, data):
        await self.__auditTransactionCommand(data)
        resp = await self.transaction.handleSellAmount(data)
        return resp

    async def handleSellTrigger(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleSellTrigger(data)
        return resp

    async def handleCancelSellTrigger(self, data):
        await self.__auditUserCommand(data)
        resp = await self.transaction.handleCancelSellTrigger(data)
        return resp
    # ----------------------------------------------------------
