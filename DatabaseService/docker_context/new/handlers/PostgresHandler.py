from time import time
from sanic.log import logger
import asyncpg

connection_string = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='daytrader', password='tothemoon', host='localhost',
        port=5432, database='trading-db')

users_table = 'users'
funds_table = 'account_balances'
stocks_table = 'stock_balances'
from_table_where_user_query = "select {columns} from {table} where user_id = '{user}';"
to_table_where_user_query = "update {table} set {fields} where user_id = '{user}';"

#TODO: Implement the handler's methods
#TODO: Return response code along with data
class PostgresHandler:

    def __init__(self, loop):
        self.loop = loop

    async def initializePool(self):
        self.pool = await asyncpg.create_pool(
            dsn = connection_string, 
            min_size = 25,
            max_size = 25,
            max_queries = 100,
            max_inactive_connection_lifetime = 0,
            loop = self.loop)

    def getPool(self):
        return self.pool

    async def handleGetFundsCommand(self, user_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'errorMessage': 'Specified user does not exist'
            }

        get_funds_query = from_table_where_user_query.format(
            columns='account_balance', 
            table=funds_table, 
            user=user_id)
            
        result = await self.fetchQuery(get_funds_query)
        
        if result == [] or result is None or len(result) != 1:
            return {
                'errorMessage': 'Unexpected error. Could not get funds.'
            }

        funds = result[0][0]
        result = {
            'funds': funds
        }
        return result


    async def handleGetStocksCommand(self, user_id, stock_id):
        return {}

    async def handleAddFundsCommand(self, user_id, funds):
        user_exists = await self._checkUserExists(user_id)
        
        if not user_exists:
            await self._addUser(user_id)

        error_resp = {'errorMessage': 'Unexpected error. Could not add funds.'}
        success_resp = {'statusMessage': 'Funds successfully added.'}
        
        curr_balance = await self.handleGetFundsCommand(user_id)
        curr_funds = curr_balance['funds']

        add_funds_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance={f}, account_reserve={r}'.format(f=funds+curr_funds, r=0), 
            user=user_id)
        
        result = await self.executeQuery(add_funds_query)

        if type(result) != str:
            return error_resp
        
        result = result.lower().split(' ')
        
        if len(result) == 2 and result[0] == 'update' and result[1] == '1':
            return success_resp

        return error_resp


    async def handleBuyStocksCommand(self, user_id, stock_id, stock_num, funds):
        return None

    async def handleSellStocksCommand(self, user_id, stock_id, stock_num, funds):
        return None

    async def executeQuery(self, query):
        result = None
        try:
            async with self.pool.acquire() as con:
                async with con.transaction():
                    result = await con.execute(query)
        except:
            pass

        return result

    async def fetchQuery(self, query):
        """ TODO: Research error semantics for this case. Should the 
        error token be None and the no match case be []? Currently, 
        [] is error and None is no match but this needs verification.
        """
        result = []
        try:
            async with self.pool.acquire() as con:
                async with con.transaction():
                    result = await con.fetch(query)
        except:
            pass

        return result

    async def closeConnection(self):
        await self.pool.close()

    async def _checkUserExists(self, user_id):
        check_user_query = from_table_where_user_query.format(
            columns='user_id',
            table=users_table, 
            user=user_id)

        result = await self.fetchQuery(check_user_query)
        return result != [] and result is not None

    async def _addUser(self, user_id):
        user_exists = await self._checkUserExists(user_id)
        
        if user_exists:
            return True

        add_user_query = "insert into {table} values ('{user}');".format(table=users_table, user=user_id)
        add_user_query = add_user_query + "insert into {table} values ('{user}', {balance}, {reserve});".format(
            table=funds_table,
            user=user_id,
            balance=0,
            reserve=0)
        result = await self.executeQuery(add_user_query)
    
        if type(result != str):
            return False

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        return len(result) == 3 and result[0] == 'insert' and result[2] == '1'