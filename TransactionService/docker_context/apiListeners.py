import aiohttp
import aioredis
import config
from sanic.log import logger
from handlers.AuditHandler import AuditHandler
from handlers.BaseLogicHandler import BaseLogicHandler
from handlers.LegacyStockServerHandler import LegacyStockServerHandler
from handlers.RedisHandler import RedisHandler
from ServiceLogic import ServiceLogic


async def initClient(app, loop):
    app.config['client'] = aiohttp.ClientSession(loop=loop)


async def closeClient(app, loop):
    await app.config['client'].close()


async def connectRedis(app, loop):
    app.config['redisPool'] = await aioredis.create_pool(
        (config.TRANSACTION_REDIS_IP, config.TRANSACTION_REDIS_PORT),
        minsize=5,
        maxsize=10,
        loop=loop
    )


async def initRedisHandler(app, loop):
    app.config['redisHandler'] = RedisHandler(app.config['redisPool'], app.config['client'], config.DATABASE_SERVER_IP,
                                              config.DATABASE_SERVER_PORT)


async def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        app.config['client'],
        config.WEB_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT
    )


async def initLegacyStock(app, loop):
    app.config['legacyStock'] = LegacyStockServerHandler(config.LEGACY_STOCK_SERVER_IP, config.LEGACY_STOCK_SERVER_PORT,
                                                         app.config['redisPool'], app.config['audit'])


async def initBaseLogic(app, loop):
    app.config['baseLogic'] = BaseLogicHandler(app.config['legacyStock'], app.config['redisPool'],
                                               app.config['redisHandler'], app.config['audit'],
                                               app.config['client'], config.DATABASE_SERVER_IP,
                                               config.DATABASE_SERVER_PORT)


async def initServiceLogic(app, loop):
    app.config['serviceLogic'] = ServiceLogic(app.config['baseLogic'], app.config['redisHandler'],
                                              app.config['legacyStock'])


async def closeRedis(app, loop):
    redis_pool = app.config['redisPool']
    redis_pool.close()
    await redis_pool.await_closed()
