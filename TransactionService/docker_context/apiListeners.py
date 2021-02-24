import aiohttp
import aioredis
import config
from sanic.log import logger
from handlers.AuditHandler import AuditHandler
from handlers.TransactionHandler import TransactionHandler
from ServiceLogic import ServiceLogic


async def initClient(app, loop):
    app.config['client'] = aiohttp.ClientSession(loop=loop)


async def closeClient(app, loop):
    await app.config['client'].close()


async def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        app.config['client'],
        config.WEB_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT
    )


async def initTransactionLogic(app, loop):
    app.config['transactionLogic'] = TransactionHandler(app.config['audit'], app.config['client'],
                                                        config.CACHE_SERVER_IP, config.CACHE_SERVER_PORT)


async def initServiceLogic(app, loop):
    app.config['serviceLogic'] = ServiceLogic(app.config['transactionLogic'], app.config['legacyStock'])


async def closeRedis(app, loop):
    redis_pool = app.config['redisPool']
    redis_pool.close()
    await redis_pool.await_closed()
