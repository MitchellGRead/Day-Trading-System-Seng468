from sanic.log import logger
from handlers.PostgresHandler import PostgresHandler
from handlers.MongoHandler import MongoHandler
from ServiceLogic import ServiceLogic

async def initDbConnections(app, loop):
    logger.debug('Creating database connections')
    app.config['psqlHandler'] = PostgresHandler(loop)
    app.config['mongoHandler'] = MongoHandler(loop)
    await app.config['psqlHandler'].initializePool()
    
def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(
        app.config['psqlHandler'],
        app.config['mongoHandler']
    )

async def closeDbConnections(app, loop):
    logger.debug('Closing database connections')
    app.config['mongoHandler'].closeConnection()
    await app.config['psqlHandler'].closeConnection()
