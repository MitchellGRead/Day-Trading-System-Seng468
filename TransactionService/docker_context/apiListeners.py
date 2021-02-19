import aiohttp
import aioredis
import config


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


async def closeRedis(app, loop):
    redis_pool = app.config['redisPool']
    redis_pool.close()
    await redis_pool.await_closed()
