from sanic.log import logger
from sanic import response

from XmlWriter import XmlWriter
from Client import Client
import json


class DbmHandler:

    def __init__(self, dbm_ip, dbm_port, loop):
        self.dbm_url = f'http://{dbm_ip}:{dbm_port}'
        self.client = Client(loop)

    async def saveAuditEvent(self, event):
        result, status = await self.client.postRequest(f'{self.dbm_url}/audit/event', event)
        if status != 200:
            logger.error(f'Failed to audit event to database - {result} - {status}')

    async def fetchAuditEvents(self, user_id=''):
        endpoint = '/dumplog'
        params = {}
        if user_id:
            params['user_id'] = user_id

        result, status = await self.client.getRequest(f'{self.dbm_url}{endpoint}', params, contentType='text')
        events = json.loads(result)
        return events, status


    async def fetchAccountSummary(self, user_id):
        endpoint = f'/summary/{user_id}'
        result, status = await self.client.getRequest(f'{self.dbm_url}{endpoint}', contentType='json')

        return result, status
