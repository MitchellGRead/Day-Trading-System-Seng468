from sanic.log import logger
from handlers.PostgresHandler import PostgresHandler
from ServiceLogic import ServiceLogic


def initDbConnections(app, loop):
    logger.debig('Creating database connections')
    app.config['psqlHandler'] = PostgresHandler(loop)

def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(
        app.config['psqlHandler']
    )

def closeDbConnections(app, loop):
    logger.debug('Closing database connections')
    app.config['psqlHandler'].closeConnection()