import aiohttp
import aioredis
import config
from sanic.log import logger
from AuditHandler import AuditHandler
from RedisHandler import RedisHandler
from CacheHandler import CacheHandler
from LegacyStockServerHandler import LegacyStockServerHandler
from ServiceLogic import ServiceLogic


async def connectRedis(app, loop):
    app.config['redisPool'] = await aioredis.create_redis_pool(
        f'redis://{config.CACHE_REDIS_IP}:{config.CACHE_REDIS_PORT}')
    await app.config['redisPool'].config_set(parameter='maxmemory', value='2gb')
    await app.config['redisPool'].config_set(parameter='maxmemory-policy', value='allkeys-lru')


async def initRedisHandler(app, loop):
    app.config['redisHandler'] = RedisHandler(
        app.config['redisPool'],
        config.DATABASE_SERVER_IP,
        config.DATABASE_SERVER_PORT,
        loop
    )


async def initAuditHandler(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        config.CACHE_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT,
        loop
    )


async def initLegacyStockHandler(app, loop):
    logger.debug('Creating legacy stock handler')
    app.config['legacyStock'] = LegacyStockServerHandler(
        config.LEGACY_STOCK_SERVER_IP,
        config.LEGACY_STOCK_SERVER_PORT,
        app.config['audit'],
        app.config['redisHandler']
    )


async def initCacheHandler(app, loop):
    logger.debug('Creating cache handler')
    app.config['cacheLogic'] = CacheHandler(
        app.config['redisPool'],
        app.config['redisHandler'],
        app.config['audit'],
        loop,
        config.DATABASE_SERVER_IP,
        config.DATABASE_SERVER_PORT,
        app.config['legacyStock']
    )


async def initServiceLogic(app, loop):
    app.config['serviceLogic'] = ServiceLogic(app.config['cacheLogic'])


async def closeRedis(app, loop):
    redis_pool = app.config['redisPool']
    redis_pool.close()
    await redis_pool.wait_closed()


async def closeHandlerClients(app, loop):
    logger.debug('Closing handler clients')
    await app.config['audit'].client.stop()
    await app.config['cacheLogic'].client.stop()
    await app.config('redisPool').client.stop()
