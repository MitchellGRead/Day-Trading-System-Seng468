import aiohttp
import aioredis
import config
from sanic.log import logger
from handlers.AuditHandler import AuditHandler
from handlers.RedisHandler import RedisHandler
from handlers.CacheHandler import CacheHandler
from handlers.LegacyStockServerHandler import LegacyStockServerHandler
from ServiceLogic import ServiceLogic


async def initClient(app, loop):
    app.config['client'] = aiohttp.ClientSession(loop=loop)


async def closeClient(app, loop):
    await app.config['client'].close()


async def connectRedis(app, loop):
    app.config['redisPool'] = await aioredis.create_redis_pool(f'redis://{config.CACHE_REDIS_IP}:{config.CACHE_REDIS_PORT}')
    await app.config['redisPool'].config_set(parameter='maxmemory', value='2gb')
    await app.config['redisPool'].config_set(parameter='maxmemory-policy', value='allkeys-lru')


async def initRedisHandler(app, loop):
    app.config['redisHandler'] = RedisHandler(app.config['redisPool'], app.config['client'],
                                              config.DATABASE_SERVER_IP,
                                              config.DATABASE_SERVER_PORT)


async def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        app.config['client'],
        config.CACHE_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT
    )


async def initLegacyStock(app, loop):
    app.config['legacyStock'] = LegacyStockServerHandler(config.LEGACY_STOCK_SERVER_IP, config.LEGACY_STOCK_SERVER_PORT,
                                                         app.config['audit'])


async def initCacheLogic(app, loop):
    app.config['cacheLogic'] = CacheHandler(app.config['redisPool'],
                                            app.config['redisHandler'], app.config['audit'],
                                            app.config['client'], config.DATABASE_SERVER_IP,
                                            config.DATABASE_SERVER_PORT, app.config['legacyStock'])


async def initServiceLogic(app, loop):
    app.config['serviceLogic'] = ServiceLogic(app.config['cacheLogic'])


async def closeRedis(app, loop):
    redis_pool = app.config['redisPool']
    redis_pool.close()
    await redis_pool.wait_closed()
