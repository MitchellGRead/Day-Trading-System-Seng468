from sanic.log import logger
from XmlWriter import XmlWriter


class ServiceLogic:

    def __init__(self, dbm_handler):
        self.dbm_handler = dbm_handler

    async def fetchAccountSummary(self, data):
        return await self.dbm_handler.fetchAccountSummary(data['user_id'])

    async def generateDumplog(self, data):
        user_id = data.get('user_id', '')
        filename = data['filename']
        result, status = await self.dbm_handler.fetchAuditEvents(user_id)

        if status != 200:
            return result, status

        xmlWriter = XmlWriter(filename)
        xmlWriter.createLogFile(result)
        return {'success': f'file {filename} generated'}, 200

    async def logEvent(self, event):
        logger.debug(f'Trying to log {event["xmlName"]} event.')
        await self.dbm_handler.saveAuditEvent(event)
