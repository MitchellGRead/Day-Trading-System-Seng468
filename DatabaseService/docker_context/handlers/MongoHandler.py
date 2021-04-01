from time import time
from sanic.log import logger
import asyncio
import motor.motor_asyncio

class MongoHandler:

    def __init__(self, loop):
        self.loop = loop
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient('mongo-db-4.4', 27017, io_loop = self.loop)
        self.mongo_db = self.mongo_client['trading-db']
        self.user_logs = self.mongo_db['logs']

    async def initializeMongo(self):
        logger.debug("Initializing Mongo")
        async with await self.mongo_client.start_session() as s:
            result = await self.user_logs.insert_one({'x':2}, session=s)
            if result.acknowledged:
                logger.debug("Successful insert into Mongo")
            else:
                logger.debug("Failed insert into Mongo")

    async def handleAddUserAuditEvent(self, user_id, audit_data):
        result = await self.__addUser(user_id)
        
        if result is False:
            return {'status': 'failure', 'message': 'Could not find user logs'}, 500
        
        result = await self.user_logs.update_one(
                {"user_id": user_id},
                { "$push": {"logs": audit_data}}
            )
        
        if result.acknowledged is False:
            return {'status': 'failure', 'message': 'Audit event write operation failed'}, 500
        
        result, status = await self.handleAddSystemAuditEvent(audit_data)
        
        return {'status': 'success', 'message': 'Added audit event to user logs'}, 200

    async def handleAddSystemAuditEvent(self, audit_data):
        result = await self.user_logs.update_one(
                {"user_id": ""},
                { "$push": {"logs": audit_data}}
            )
        
        if result.acknowledged is False:
            return {'status': 'failure', 'message': 'Audit event write operation failed'}, 500

        return {'status': 'success', 'message': 'Added audit event to system logs'}, 200

    async def __checkUserExists(self, user_id):
        userDoc = await self.user_logs.find_one({"user_id": user_id})
        return userDoc is not None

    async def __addUser(self, user_id):
        user_exists = await self.__checkUserExists(user_id)

        if user_exists:
            return True
        
        async with await self.mongo_client.start_session() as s:
            result = await self.user_logs.insert_one({"user_id": user_id, "logs": [""]}, session=s)
            return result.acknowledged
