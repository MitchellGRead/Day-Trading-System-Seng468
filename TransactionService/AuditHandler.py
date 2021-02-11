from EventTypes import UserCommandEvent, AccountTransaction, ErrorEvent, QuoteServerEvent
import pickle


class AuditHandler:

    def __init__(self, conn, service_name):
        self.audit_conn = conn
        self.service_name = service_name

    def sendAndRecvObject(self, obj):
        self.audit_conn.sendall(pickle.dumps(obj))
        data = self.audit_conn.recv(4096)
        return pickle.loads(data)

    def handleAddEvent(self, transaction_num, user_name, funds):
        audit_event = UserCommandEvent(
            server=self.service_name,
            transactionNumber=transaction_num,
            command='ADD',
            userName=user_name,
            funds=funds,
        )
        resp = self.sendAndRecvObject(audit_event)

        audit_event = AccountTransaction(
            server=self.service_name,
            transactionNumber=transaction_num,
            action='add',
            userName=user_name,
            funds=funds
        )
        resp = self.sendAndRecvObject(audit_event)

    def handleErrorEvent(self, transaction_num, command, error_msg, user_name='',
                         stock_symbol='', filename='', funds=0, ):
        audit_event = ErrorEvent(
            server=self.service_name,
            transactionNumber=transaction_num,
            command=command,
            errorMessage=error_msg,
            userName=user_name,
            stockSymbol=stock_symbol,
            filename=filename,
            funds=funds
        )
        resp = self.sendAndRecvObject(audit_event)

    def handleQuoteEvent(self, transaction_num, quote_server_time, user_name,
                         stock_symbol, price, crptokey):
        audit_event = QuoteServerEvent(
            server=self.service_name,
            quoteServerTimestamp=quote_server_time,
            transactionNumber=transaction_num,
            userName=user_name,
            stockSymbol=stock_symbol,
            price=price,
            cryptoKey=crptokey
        )
        resp = self.sendAndRecvObject(audit_event)

    def handleUserCommandEvent(self, transaction_num, command, user_name, funds=0,
                               stock_symbol='', filename=''):
        if command == 'DUMPLOG':
            audit_event = UserCommandEvent(
                server=self.service_name,
                transactionNumber=transaction_num,
                command=command,
                userName=user_name,
                filename=filename
            )
            resp = self.sendAndRecvObject(audit_event)
        else:
            audit_event = UserCommandEvent(
                server=self.service_name,
                transactionNumber=transaction_num,
                command=command,
                userName=user_name,
                stockSymbol=stock_symbol,
                funds=funds
            )
            resp = self.sendAndRecvObject(audit_event)
