from EventTypes import UserCommandEvent, ErrorEvent, SystemEvent
import pickle


class AuditHandler:

    def __init__(self, conn, service_name):
        self.audit_conn = conn
        self.service_name = service_name

    def sendAndRecvObject(self, obj):
        self.audit_conn.sendall(pickle.dumps(obj))
        data = self.audit_conn.recv(4096)
        return pickle.loads(data)

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
        return self.sendAndRecvObject(audit_event)

    def handleSystemEvent(self, transaction_num, command, user_name='', stock_symbol='',
                          filename='', funds=0):
        audit_event = SystemEvent(
            server=self.service_name,
            transactionNumber=transaction_num,
            command=command,
            userName=user_name,
            stockSymbol=stock_symbol,
            funds=funds,
            filename=filename
        )
        resp = self.sendAndRecvObject(audit_event)

    def handleUserCommandEvent(self, transaction_num, command, user_name, filename=''):
        if command == 'DUMPLOG':
            audit_event = UserCommandEvent(
                server=self.service_name,
                transactionNumber=transaction_num,
                command=command,
                userName=user_name,
                filename=filename
            )
            resp = self.sendAndRecvObject(audit_event)
        elif command == 'DISPLAY_SUMMARY':
            audit_event = UserCommandEvent(
                server=self.service_name,
                transactionNumber=transaction_num,
                command=command,
                userName=user_name,
            )
            resp = self.sendAndRecvObject(audit_event)
        else:
            err = f'Invalid command {command} sent from {self.service_name}. ' \
                  f'to audit service. Should this have been sent to transaction service?'
            self.handleErrorEvent(
                transaction_num=transaction_num,
                command=command,
                error_msg=err,
                user_name=user_name,
                filename=filename
            )
            resp = {
                'status': 400,
                'reason': err,
                'content': ''
            }
        return resp
