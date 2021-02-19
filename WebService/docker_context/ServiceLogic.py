
class ServiceLogic:

    def __init__(self, client, audit):
        self.client = client
        self.audit = audit

    async def auditTransactionCommand(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id'],
            stock_symbol=data['stock_symbol'],
            amount=data['amount'],
        )

    async def auditUserCommand(self, data):
        await self.audit.handleUserCommand(
            trans_num=data['transaction_num'],
            command=data['command'],
            user_id=data['user_id']
        )

    async def handleQuote(self, data):
        # Auditing is handled in transaction service
        # TODO send command to transaction service
        return

    async def handleDisplaySummary(self, data):
        await self.auditUserCommand(data)
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
        # TODO send to transaction service
        return

    # BUY COMMAND HANDLING -------------------------------------
    async def handleBuy(self, data):
        await self.auditTransactionCommand(data)
        # TODO send to transaction service
        return

    async def handleCommitBuy(self, data):
        await self.auditUserCommand(data)
        # TODO send to transaction service
        return

    async def handleCancelBuy(self, data):
        await self.auditUserCommand(data)
        # TODO send to transaction service
        return
    # ----------------------------------------------------------

    # SELL COMMAND HANDLING -------------------------------------
    async def handleSell(self, data):
        await self.auditTransactionCommand(data)
        # TODO send to transaction service
        return

    async def handleCommitSell(self, data):
        await self.auditUserCommand(data)
        # TODO send to transaction service
        return

    async def handleCancelSell(self, data):
        await self.auditUserCommand(data)
        # TODO send to transaction service
        return
    # ----------------------------------------------------------

    # BUY TRIGGER COMMAND HANDLING -----------------------------
    async def handleBuyAmount(self, data):
        await self.auditTransactionCommand(data)
        # TODO send to trigger service
        return

    async def handleBuyTrigger(self, data):
        await self.auditUserCommand(data)
        # TODO send to trigger service
        return

    async def handleCancelBuyTrigger(self, data):
        await self.auditUserCommand(data)
        # TODO send to trigger service
        return
    # ----------------------------------------------------------

    # SELL TRIGGER COMMAND HANDLING ----------------------------
    async def handleSellAmount(self, data):
        await self.auditTransactionCommand(data)
        # TODO send to trigger service
        return

    async def handleSellTrigger(self, data):
        await self.auditUserCommand(data)
        # TODO send to trigger service
        return

    async def handleCancelSellTrigger(self, data):
        await self.auditUserCommand(data)
        # TODO send to trigger service
        return
    # ----------------------------------------------------------
