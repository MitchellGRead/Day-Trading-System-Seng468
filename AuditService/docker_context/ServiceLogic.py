from sanic.log import logger
from XmlWriter import XmlWriter


class ServiceLogic:

    def __init__(self, dbm_handler):
        self.dbm_handler = dbm_handler

    async def fetchAccountSummary(self, data):
        return self.dbm_handler.fetchAccountSummary(data['user_id'])

    async def generateDumplog(self, data):
        user_id = data.get('user_id', '')
        filename = data['filename']
        events = self.dbm_handler.fetchAuditEvents(user_id)

        xml_writer = XmlWriter(filename)
        xml_writer.createLogFile(events)
        return {'success': f'file {filename} generated'}

    async def logEvent(self, event):
        logger.debug(f'Trying to log {event["xmlName"]} event.')
        self.dbm_handler.saveAuditEvent(event)
