from sanic.log import logger
from XmlWriter import XmlWriter


class ServiceLogic:
    # These lists are temporary and are meant to be stored in a DB on a per user basis in Mongo
    log_events = []

    async def __logUserCommandEvent(self, event):
        self.log_events.append(event)
        if event['command'] == 'DUMPLOG':
            logger.debug(event)
            await self.__dumplog(event['filename'], event.get('user_id', ''))

    async def __logAccountTransactionEvent(self, event):
        self.log_events.append(event)

    async def __logSystemEvent(self, event):
        self.log_events.append(event)

    async def __logQuoteServerEvent(self, event):
        self.log_events.append(event)

    async def __logErrorEvent(self, event):
        self.log_events.append(event)

    # Signature will likely change
    async def __dumplog(self, filename, user_id=''):
        xml_writer = XmlWriter(filename)
        # get request to DBM and provide a user_id if one exists
        xml_writer.createLogFile(self.log_events)

    async def logEvent(self, event):
        xml_tag = event['xmlName']
        logger.debug(f'Trying to log {xml_tag} event.')

        if xml_tag == 'userCommand':
            await self.__logUserCommandEvent(event)
        elif xml_tag == 'accountTransaction':
            await self.__logAccountTransactionEvent(event)
        elif xml_tag == 'systemEvent':
            await self.__logSystemEvent(event)
        elif xml_tag == 'quoteServer':
            await self.__logQuoteServerEvent(event)
        elif xml_tag == 'errorEvent':
            await self.__logErrorEvent(event)
        else:
            logger.error(f'AuditHandler: The xml tag - {xml_tag} is not valid. Skipping event.')
            return False
        return True
