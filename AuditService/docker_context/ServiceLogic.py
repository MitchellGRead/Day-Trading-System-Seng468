from sanic.log import logger
from XmlWriter import XmlWriter


class ServiceLogic:

    def __init__(self, dbm_handler):
        self.dbm_handler = dbm_handler

    async def fetchAccountSummary(self, data):
        return self.dbm_handler.fetchAccountSummary(data['user_id'])

    # Signature will likely change
    async def __dumplog(self, filename, user_id=''):
        xml_writer = XmlWriter(filename)
        # get request to DBM and provide a user_id if one exists
        xml_writer.createLogFile(self.log_events)

    async def logEvent(self, event):
        logger.debug(f'Trying to log {event["xmlName"]} event.')
        self.dbm_handler.saveAuditEvent(event)
