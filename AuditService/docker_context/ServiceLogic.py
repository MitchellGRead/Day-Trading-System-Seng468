from XmlWriter import XmlWriter


class AuditHandler:
    # These lists are temporary and are meant to be stored in a DB on a per user basis in Mongo
    log_events = []

    def logUserCommandEvent(self, user_command_event):
        if user_command_event.xmlName != 'userCommand':
            print(f'invalid command event provided - {user_command_event}')
            return None
        self.log_events.append(user_command_event)

    def logAccountTransactionEvent(self, acc_transaction_event):
        if acc_transaction_event.xmlName != 'accountTransaction':
            print(f'invalid command event provided - {acc_transaction_event}')
            return None
        self.log_events.append(acc_transaction_event)

    def logSystemEvent(self, system_event):
        if system_event.xmlName != 'systemEvent':
            print(f'invalid command event provided - {system_event}')
            return None
        self.log_events.append(system_event)

    def logQuoteServerEvent(self, quote_server_event):
        if quote_server_event.xmlName != 'quoteServer':
            print(f'invalid command event provided - {quote_server_event}')
            return None
        self.log_events.append(quote_server_event)

    def logErrorEvent(self, error_event):
        if error_event.xmlName != 'errorEvent':
            print(f'invalid command event provided - {error_event}')
            return None
        self.log_events.append(error_event)

    def logDebugEvent(self, debug_event):
        if debug_event.xmlName != 'debugEvent':
            print(f'invalid command event provided - {debug_event}')
            return None
        self.log_events.append(debug_event)

    # Signature will change
    def dumplog(self, filename=''):
        xml_writer = XmlWriter(filename)
        xml_writer.createLogFile(self.log_events)
        return None

    # Signature will change
    def displaySummary(self):
        # get user data
        # send back an object/dataclass?
        return None

    def logEvent(self, event):
        xml_tag = event.xmlName
        if xml_tag == 'userCommand':
            self.logUserCommandEvent(event)
        elif xml_tag == 'accountTransaction':
            self.logAccountTransactionEvent(event)
        elif xml_tag == 'systemEvent':
            self.logSystemEvent(event)
        elif xml_tag == 'quoteServer':
            self.logQuoteServerEvent(event)
        elif xml_tag == 'errorEvent':
            self.logErrorEvent(event)
        else:
            print(f'AuditHandler: The xml tag - {xml_tag} is not valid. Skipping event.')
            return False
        return True
