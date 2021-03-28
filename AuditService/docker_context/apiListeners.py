from sanic.log import logger
from ServiceLogic import ServiceLogic
from sanic.log import logger

from ServiceLogic import ServiceLogic

import config
from DbmHandler import DbmHandler

async def initDbmHanlder(app, loop):
    logger.debug('Creating DBM Handler')
    app.config['dbm'] = DbmHandler(
        config.DATABASE_SERVER_IP,
        config.DATABASE_SERVER_PORT,
        loop
    )

def initServiceLogic(app, loop):
    logger.debug('Creating api logic')
    app.config['logic'] = ServiceLogic(app.config['dbm'])
