
class XmlWriter:
    SAVE_PATH = 'logfiles/'

    def __init__(self, file_name=''):
        if file_name and file_name.endswith('.xml'):
            self.save_location = f'{self.SAVE_PATH}{file_name}'
        else:
            self.save_location = f'{self.SAVE_PATH}logfile.xml'

    def writeUserCommand(self, event):
        log = self.writeCommon(event) + \
              f'\t\t<command>{event.command}</command>\n'

        if event.funds:
            log += f'\t\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n'
        if event.filename:
            log += f'\t\t<filename>{event.filename}</filename>\n'
        if event.stockSymbol:
            log += f'\t\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n'

        log += f'\t</{event.xmlName}>\n'
        return log

    def writeAccountTransaction(self, event):
        log = self.writeCommon(event) + \
              f'\t\t<action>{event.action}</action>\n' \
              f'\t\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n' \
              f'\t</{event.xmlName}>\n'

        return log

    def writeSystemEvent(self, event):
        log = self.writeCommon(event) + \
              f'\t\t<command>{event.command}</command>\n'

        if event.stockSymbol:
            log += f'\t\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n'
        if event.funds:
            log += f'\t\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n'
        if event.filename:
            log += f'\t\t<filename>{event.filename}</filename>\n'

        log += f'\t</{event.xmlName}>\n'

        return log

    def writeQuoteServerEvent(self, event):
        log = self.writeCommon(event) + \
              f'\t\t<quoteServerTime>{event.quoteServerTimestamp}</quoteServerTime>\n' \
              f'\t\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n' \
              f'\t\t<price>{self.ensureTrailingZeros(event.price)}</price>\n' \
              f'\t\t<cryptokey>{event.cryptoKey}</cryptokey>\n' \
              f'\t</{event.xmlName}>\n'

        return log

    def writeErrorEvent(self, event):
        log = self.writeCommon(event) + \
            f'\t\t<errorMessage>{event.errorMessage}</errorMessage>\n' \
            f'\t\t<command>{event.command}</command>\n'

        if event.stockSymbol:
            log += f'\t\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n'
        if event.filename:
            log += f'\t\t<filename>{event.filename}</filename>\n'
        if event.funds:
            log += f'\t\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n'

        log += f'\t</{event.xmlName}>\n'
        return log

    def writeCommon(self, event):
        log = f'\t<{event.xmlName}>\n' \
               f'\t\t<timestamp>{event.timestamp}</timestamp>\n' \
               f'\t\t<server>{event.server}</server>\n' \
               f'\t\t<transactionNum>{event.transactionNumber}</transactionNum>\n'

        if event.userName:
            log += f'\t\t<username>{event.userName}</username>\n'

        return log

    def ensureTrailingZeros(self, num):
        return '%.2f' % num

    def createLogFile(self, audit_events):
        content = '<?xml version=\"1.0\"?>\n' \
                 '<log>\n'

        for event in audit_events:
            xml_tag = event.xmlName
            if xml_tag == 'userCommand':
                content += self.writeUserCommand(event)
            elif xml_tag == 'accountTransaction':
                content += self.writeAccountTransaction(event)
            elif xml_tag == 'systemEvent':
                content += self.writeSystemEvent(event)
            elif xml_tag == 'quoteServer':
                content += self.writeQuoteServerEvent(event)
            elif xml_tag == 'errorEvent':
                content += self.writeErrorEvent(event)
            else:
                print(f'XmlWriter: The xml tag - {xml_tag} is not valid. Skipping event.')

        content += '</log>\n'
        with open(self.save_location, 'w') as file:
            file.write(content)


