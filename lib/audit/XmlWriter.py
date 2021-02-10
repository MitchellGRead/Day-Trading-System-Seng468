
class XmlWriter:
    SAVE_PATH = '../../AuditService/logfiles/'

    def __init__(self, file_name=''):
        if file_name and file_name.endswith('.xml'):
            self.file_name = file_name
        else:
            self.file_name = 'logfile.xml'

    def writeUserCommand(self, event):
        log = self.writeCommon(event) + \
              f'\t<command>{event.command}</command>\n'

        if event.funds:
            log += f'\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n'
        if event.filename:
            log += f'\t<filename>{event.filename}</filename>\n'
        if event.stockSymbol:
            log += f'\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n'

        log += f'<{event.xmlName}>\n'
        return log

    def writeAccountTransaction(self, event):
        log = self.writeCommon(event) + \
              f'\t<action>{event.action}</action>\n' \
              f'\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n' \
              f'</{event.xmlName}>\n'

        return log

    def writeSystemEvent(self, event):
        log = self.writeCommon(event) + \
              f'\t<command>{event.command}</command>\n'

        if event.stockSymbol:
            log += f'\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n'
        if event.funds:
            log += f'\t<funds>{self.ensureTrailingZeros(event.funds)}</funds>\n'
        if event.filename:
            log += f'\t<filename>{event.filename}</filename>\n'

        log += f'</{event.xmlName}>\n'

        return log

    def writeQuoteServerEvent(self, event):
        log = self.writeCommon(event) + \
              f'\t<quoteServerTime>{event.quoteServerTimestamp}</quoteServerTime>\n' \
              f'\t<stockSymbol>{event.stockSymbol}</stockSymbol>\n' \
              f'\t<price>{self.ensureTrailingZeros(event.price)}</price>\n' \
              f'\t<cryptokey>{event.cryptokey}</cryptokey>\n' \
              f'</{event.xmlName}>\n'

        return log

    def writeErrorEvent(self, event):
        log = self.writeCommon(event) + \
            f'\t<errorMessage>{event.errorMessage}</errorMessage>\n' \
            f'\t<command>{event.command}</command>\n'

        if event.stockSymbol:
            log += f'\t<stockSymbol>{event.stockSymbol}</stockSymbol\n'
        if event.filename:
            log += f'\t<filename>{event.filename}</filename\n'
        if event.funds:
            log += f'\t<funds>{self.ensureTrailingZeros(event.funds)}</funds\n'

        log += f'</{event.xmlName}>\n'
        return log

    def writeCommon(self, event):
        log = f'<{event.xmlName}>\n' \
               f'\t<timestamp>{event.timestamp}</timestamp>\n' \
               f'\t<server>{event.server}</server>\n' \
               f'\t<transactionNum>{event.transactionNumber}</transactionNum\n'

        if event.userName:
            log += f'\t<username>{event.userName}</username>\n'

        return log

    def ensureTrailingZeros(self, num):
        return '%.2f' % num

