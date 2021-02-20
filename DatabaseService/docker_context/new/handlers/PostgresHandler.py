from time import time
from sanic.log import logger
import asyncpg

connection_string = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='daytrader', password='tothemoon', host='localhost',
        port=5432, database='trading-db')

users_table = "users"
funds_table = "account_balances"
stocks_table = "stock_balances"

#TODO: Implement the handler's methods
class PostgresHandler:

    def __init__(self, loop):
        self.pool = asyncpg.create_pool(
            dsn = connection_string, 
            min_size = 25,
            max_size = 25,
            max_queries = 100,
            max_inactive_connection_lifetime = 0,
            loop = loop)

        # async with self.pool.acquire() as con:
        #     test = await con.fetchval("SELECT * from users;")

    def getPool(self):
        return self.pool

    async def handleGetFundsCommand(self, user_id):
        return None

    async def handleGetStocksCommand(self, user_id, stock_id):
        return None

    async def handleAddFundsCommand(self, data):
        return None

    async def handleBuyStocksCommand(self, data):
        return None

    async def handleSellStocksCommand(self, data):
        return None

    async def executeQuery(self, query):
        async with self.pool.acquire() as con:
            async with con.transaction() as trans:
                await con.execute(query)
                return True

        return False

    async def fetchQuery(self, query):
        async with self.pool.acquire() as con:
            async with con.transaction() as trans:
                result = await con.fetch(query)
                return result

        return []

    async def closeConnection(self):
        await self.pool.close()
