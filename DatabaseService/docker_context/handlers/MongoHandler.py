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
    
    async def handleGetDumplogCommand(self, user_id):
        userExists = True if user_id == "" else False
        if not userExists:
            userExists = await self.__checkUserExists(user_id)

        if not userExists:
            return {'errorMessage': 'User not found.'}, 404

        logsDoc = None
        try:
            logsDoc = await self.user_logs.find_one({"user_id": user_id})
        except Exception as e:
            logsDoc = None
            logger.error(f'Encountered error while getting user dumplogs for user {user_id}. Exception: {e.message}')

        if logsDoc is None:
            return {'errorMessage': 'Could not get dumplog'}, 500
        elif 'logs' not in logsDoc:
            return {'errorMessage': 'Could not find logs'}, 500

        logs = logsDoc['logs']

        if logs == []:
            return {'errorMessage': 'No logs exist in the system'}, 404
    
        return logs, 200

    async def handleAddUserAuditEvent(self, user_id, audit_data):
        result = await self.__addUser(user_id)
        
        if result is False:
            return {'status': 'failure', 'message': 'Could not find user logs'}, 500
        
        try:
            result = await self.user_logs.update_one(
                    {"user_id": user_id},
                    { "$push": {"logs": audit_data}}
                )
        except Exception as e:
            result = None
            logger.error(f'Encountered error while adding user audit event for user {user_id}. Exception: {e.message}')

        if result is None or result.acknowledged is False:
            return {'status': 'failure', 'message': 'Audit event write operation failed'}, 500
        
        result, status = await self.handleAddSystemAuditEvent(audit_data)
        
        return {'status': 'success', 'message': 'Added audit event to user logs'}, 200

    async def handleAddSystemAuditEvent(self, audit_data):
        try:
            result = await self.user_logs.update_one(
                    {"user_id": ""},
                    { "$push": {"logs": audit_data}}
                )
        except Exception as e:
            result = None
            logger.error(f'Encountered error while adding system audit event. Exception: {e.message}')
        
        if result is None or result.acknowledged is False:
            return {'status': 'failure', 'message': 'Audit event write operation failed'}, 500

        return {'status': 'success', 'message': 'Added audit event to system logs'}, 200

    def closeConnection(self):
        self.mongo_client.close()

    async def __checkUserExists(self, user_id):
        userDoc = await self.user_logs.find_one({"user_id": user_id})
        return userDoc is not None

    async def __addUser(self, user_id):
        user_exists = await self.__checkUserExists(user_id)

        if user_exists:
            return True
        
        result = await self.user_logs.insert_one({"user_id": user_id, "logs": []}) 
        return result.acknowledged
