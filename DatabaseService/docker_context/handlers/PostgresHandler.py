from time import time
from sanic.log import logger
import asyncpg

connection_string = "postgres://{user}:{password}@{host}:{port}/{database}".format(
    user='daytrader', password='tothemoon', host='trading-db-13',
    port=5432, database='trading-db')

users_table = 'users'
funds_table = 'account_balances'
stocks_table = 'stock_balances'
from_table_where_user_query = "select {columns} from {table} where user_id = '{user}';"
from_table_where_query = "select {columns} from {table} {where};"
to_table_where_user_query = "update {table} set {fields} where user_id = '{user}';"


# TODO: Implement the handler's methods
# TODO: Return response code along with data
class PostgresHandler:

    def __init__(self, loop):
        self.loop = loop

    async def initializePool(self):
        self.pool = await asyncpg.create_pool(
            dsn=connection_string,
            min_size=25,
            max_size=25,
            max_queries=100,
            max_inactive_connection_lifetime=0,
            loop=self.loop)

    def getPool(self):
        return self.pool

    async def handleGetAllFundsCommand(self):
        get_funds_query = from_table_where_query.format(
            columns='*',
            table=funds_table,
            where=''
        )

        result = await self.fetchQuery(get_funds_query)

        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get funds.'
            }

        resp_list = {}
        for record in result:
            resp_list[record[0]] = {'available_funds': record[1], 'reserved_funds': record[2]}

        return resp_list

    async def handleGetUserFundsCommand(self, user_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'errorMessage': 'Specified user does not exist'
            }

        get_funds_query = from_table_where_user_query.format(
            columns='*',
            table=funds_table,
            user=user_id)

        result = await self.fetchQuery(get_funds_query)

        if result == [] or result is None or len(result) != 1:
            return {
                'errorMessage': 'Unexpected error. Could not get funds.'
            }

        available_funds = result[0][1]
        reserved_funds = result[0][2]
        result = {
            'available_funds': available_funds,
            'reserved_funds': reserved_funds
        }
        return result

    async def handleGetAllStocksCommand(self):
        get_stocks_query = from_table_where_query.format(
            columns='*',
            table=stocks_table,
            where=''
        )

        result = await self.fetchQuery(get_stocks_query)
        logger.debug(str(result))
        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get stocks.'
            }

        resp_list = {}
        for record in result:
            stocks_list = {}
            if record[0] in resp_list:
                stocks_list = resp_list[record[0]]

            stocks_list[record[1]] = [record[2], record[3]]
            resp_list[record[0]] = stocks_list

        return resp_list

    async def handleGetUserStocksCommand(self, user_id, stock_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'errorMessage': 'Specified user does not exist.'
            }

        where_clause = "where user_id = '{user}'".format(user=user_id)

        if (stock_id):
            where_clause = where_clause + " AND stock_id = '{stock}'".format(stock=stock_id)

        get_stocks_query = from_table_where_query.format(columns='*', table=stocks_table, where=where_clause)

        result = await self.fetchQuery(get_stocks_query)

        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get stocks.'
            }

        resp_list = {}
        for record in result:
            resp_list[record[1]] = [record[2], record[3]]

        return resp_list

    async def handleAddFundsCommand(self, user_id, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            await self._addUser(user_id)

        error_resp = {'status': 'failure', 'message': 'Unexpected error. Could not add funds.'}
        success_resp = {'status': 'success', 'message': 'Funds successfully added.'}

        balances = await self.handleGetUserFundsCommand(user_id)
        curr_funds = balances['available_funds']

        add_funds_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance={f}'.format(f=funds + curr_funds),
            user=user_id)

        result = await self.executeQuery(add_funds_query)

        if type(result) != str:
            return error_resp

        result = result.lower().split(' ')

        if len(result) == 2 and result[0] == 'update' and result[1] == '1':
            return success_resp

        return error_resp

    async def handleBuyStocksCommand(self, user_id, stock_id, stock_num, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }

        balances = await self.handleGetUserFundsCommand(user_id)
        curr_funds = balances['available_funds']

        stocks = await self.handleGetUserStocksCommand(user_id, stock_id)
        available_stock = 0
        reserved_stock = 0

        if len(stocks) >= 2:
            available_stock = stocks[stock_id][0]
            reserved_stock = stocks[stock_id][1]

        if curr_funds < funds:
            return {
                'status': 'failure', 'message': 'Not enough funds in account.'
            }

        buy_stock_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance = {f}'.format(f=curr_funds - funds),
            user=user_id
        )
        buy_stock_query = buy_stock_query + \
                          "insert into {table} values ('{user}', '{stock}', {stock_amount}, {stock_res}) on conflict (user_id, stock_id) do update" \
                          " set stock_balance={new_balance};".format(
                              table=stocks_table,
                              user=user_id,
                              stock=stock_id,
                              stock_amount=available_stock + stock_num,
                              stock_res=reserved_stock,
                              new_balance=available_stock + stock_num
                          )

        result = await self.executeQuery(buy_stock_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not buy stocks.'
            }

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully bought stocks.'
            }

        return {
            'status': 'failure', 'message': 'Failed to update user account.'
        }

    async def handleSellStocksCommand(self, user_id, stock_id, stock_num, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }

        balances = await self.handleGetUserFundsCommand(user_id)
        curr_funds = balances['available_funds']

        stocks = await self.handleGetUserStocksCommand(user_id, stock_id)
        available_stock = 0
        reserved_stock = 0

        if len(stocks) >= 1:
            available_stock = stocks[stock_id][0]
            reserved_stock = stocks[stock_id][1]

            if available_stock < stock_num:
                return {
                    'status': 'failure', 'message': 'Not enough stocks in account.'
                }

        sell_stock_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance = {f}'.format(f=curr_funds + funds),
            user=user_id
        )
        sell_stock_query = sell_stock_query + \
                           "insert into {table} values ('{user}', '{stock}', {stock_amount}, {stock_res}) on conflict (user_id, stock_id) do update" \
                           " set stock_balance={stock_amount};".format(
                               table=stocks_table,
                               user=user_id,
                               stock=stock_id,
                               stock_amount=available_stock - stock_num,
                               stock_res=reserved_stock
                           )

        result = await self.executeQuery(sell_stock_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not sell stocks.'
            }

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully sold stocks.'
            }

        return {
            'status': 'failure', 'message': 'Failed to update user account.'
        }

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
        result = None
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
        result = await self.executeQuery(add_user_query)

        if type(result) != str:
            return False

        add_user_query = "insert into {table} values ('{user}', {balance}, {reserve});".format(
            table=funds_table,
            user=user_id,
            balance=0,
            reserve=0)
        result = await self.executeQuery(add_user_query)

        if type(result) != str:
            return False

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        return len(result) == 3 and result[0] == 'insert' and result[2] == '1'
