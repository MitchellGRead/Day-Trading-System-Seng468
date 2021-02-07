
class AuditHandler:

    # These lists are temporary and are meant to be stored in a DB on a per user basis in Mongo
    user_command_logs = []
    account_transaction_logs = []
    system_logs = []
    quote_server_logs = []
    error_logs = []
    debug_logs = []

    def logUserCommandEvent(self, user_command_event):
        if user_command_event.xmlName != 'userCommand':
            print(f'invalid command event provided - {user_command_event}')
            return None
        self.user_command_logs.append(user_command_event)

    def logAccountTransactionEvent(self, acc_transaction_event):
        if acc_transaction_event.xmlName != 'accountTransaction':
            print(f'invalid command event provided - {acc_transaction_event}')
            return None
        self.account_transaction_logs.append(acc_transaction_event)

    def logSystemEvent(self, system_event):
        if system_event.xmlName != 'systemEvent':
            print(f'invalid command event provided - {system_event}')
            return None
        self.system_logs.append(system_event)

    def logQuoteServerEvent(self, quote_server_event):
        if quote_server_event.xmlName != 'quoteServer':
            print(f'invalid command event provided - {quote_server_event}')
            return None
        self.quote_server_logs.append(quote_server_event)

    def logErrorEvent(self, error_event):
        if error_event.xmlName != 'errorEvent':
            print(f'invalid command event provided - {error_event}')
            return None
        self.error_logs.append(error_event)

    def logDebugEvent(self, debug_event):
        if debug_event.xmlName != 'debugEvent':
            print(f'invalid command event provided - {debug_event}')
            return None
        self.debug_logs.append(debug_event)

    # Signature will change
    def dumplog(self, filename):
        # get user data/event logs
        # send data to text writer
        # return the file?
        return None

    # Signature will change
    def displaySummary(self):
        # get user data
        # send back an object/dataclass?
        return None
