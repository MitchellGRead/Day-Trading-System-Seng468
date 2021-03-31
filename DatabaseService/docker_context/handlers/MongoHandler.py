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
        pass
        logger.debug("Initializing Mongo")
        async with await self.mongo_client.start_session() as s:
            result = await self.user_logs.insert_one({'x':2}, session=s)
            if result.acknowledged:
                logger.debug("Successful insert into Mongo")
            else:
                logger.debug("Failed insert into Mongo")

    async def handleAddLogToUser(self, log):
        pass

    async def __checkUserExists(self, user_id):
        pass

    async def __addUser(self, user_id):
        pass
