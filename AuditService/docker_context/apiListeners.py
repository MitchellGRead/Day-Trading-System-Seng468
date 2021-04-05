from sanic.log import logger

import config
from DbmHandler import DbmHandler
from ServiceLogic import ServiceLogic


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
