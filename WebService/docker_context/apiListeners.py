import aiohttp
import asyncio
from sanic.log import logger

import config
from ServiceLogic import ServiceLogic
from audit.AuditHandler import AuditHandler


async def initClient(app, loop):
    logger.debug('Starting http client')
    app.config['sem'] = asyncio.Semaphore(200, loop=loop)
    app.config['client'] = aiohttp.ClientSession(loop=loop)


async def closeClient(app, loop):
    await app.config['client'].close()


def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        app.config['client'],
        config.WEB_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT
    )


def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(
        app.config['client'],
        app.config['audit'],
        app.config['sem']
    )
