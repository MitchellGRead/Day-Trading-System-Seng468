from sanic.log import logger
from handlers.PostgresHandler import PostgresHandler
from ServiceLogic import ServiceLogic


async def initDbConnections(app, loop):
    logger.debug('Creating database connections')
    app.config['psqlHandler'] = PostgresHandler(loop)
    await app.config['psqlHandler'].initializePool()

def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(
        app.config['psqlHandler']
    )

async def closeDbConnections(app, loop):
    logger.debug('Closing database connections')
    await app.config['psqlHandler'].closeConnection()