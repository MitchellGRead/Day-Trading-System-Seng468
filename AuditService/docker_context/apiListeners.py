import aiohttp
from sanic.log import logger
from ServiceLogic import ServiceLogic


async def initClient(app, loop):
    logger.debug('Starting http client')
    app.config['client'] = aiohttp.ClientSession(loop=loop)


async def closeClient(app, loop):
    await app.config['client'].close()


def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic()
