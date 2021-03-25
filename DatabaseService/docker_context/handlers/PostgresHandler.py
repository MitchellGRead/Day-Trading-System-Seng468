from time import time
from sanic.log import logger
from decimal import *
import asyncpg
import asyncio

connection_string = "postgres://{user}:{password}@{host}:{port}/{database}".format(
    user='daytrader', password='tothemoon', host='trading-db-13',
    port=5432, database='trading-db')

users_table = 'users'
funds_table = 'account_balances'
stocks_table = 'stock_balances'
pending_buy_triggers_table = 'pending_buy_triggers'
pending_sell_triggers_table = 'pending_sell_triggers'
buy_triggers_table = 'complete_buy_triggers'
sell_triggers_table = 'complete_sell_triggers'
from_table_where_user_query = "select {columns} from {table} where user_id = '{user}';"
from_table_where_query = "select {columns} from {table} {where};"
to_table_where_user_query = "update {table} set {fields} where user_id = '{user}';"
to_table_where_query = "update {table} set {fields} {where};"

getcontext().prec = 20

class PostgresHandler:

    def __init__(self, loop):
        self.loop = loop
        self.pool = None

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
            }, 500

        resp_list = {}
        for record in result:
            resp_list[record[0]] = {'available_funds': record[1], 'reserved_funds': record[2]}

        return resp_list, 200

    async def handleGetUserFundsCommand(self, user_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'errorMessage': 'Specified user does not exist'
            }, 404

        get_funds_query = from_table_where_user_query.format(
            columns='*',
            table=funds_table,
            user=user_id)

        result = await self.fetchQuery(get_funds_query)

        # This is an error as empty list indicates user does not exist, a contradiction
        # of the earlier check which means something has gone wrong.
        if result == [] or result is None or len(result) != 1:
            return {
                'errorMessage': 'Unexpected error. Could not get funds.'
            }, 500

        available_funds = result[0][1]
        reserved_funds = result[0][2]
        result = {
            'available_funds': available_funds,
            'reserved_funds': reserved_funds
        }
        return result, 200

    async def handleGetAllStocksCommand(self):
        get_stocks_query = from_table_where_query.format(
            columns='*',
            table=stocks_table,
            where=''
        )

        result = await self.fetchQuery(get_stocks_query)
        
        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get stocks.'
            }, 404

        resp_list = {}
        for record in result:
            stocks_list = {}
            if record[0] in resp_list:
                stocks_list = resp_list[record[0]]

            stocks_list[record[1]] = [record[2], record[3]]
            resp_list[record[0]] = stocks_list

        return resp_list, 200

    async def handleGetUserStocksCommand(self, user_id, stock_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'errorMessage': 'Specified user does not exist.'
            }, 404

        where_clause = "where user_id = '{user}'".format(user=user_id)

        if (stock_id):
            where_clause = where_clause + " AND stock_id = '{stock}'".format(stock=stock_id)

        get_stocks_query = from_table_where_query.format(columns='*', table=stocks_table, where=where_clause)

        result = await self.fetchQuery(get_stocks_query)

        if result == []:
            return {'errorMessage': 'Stocks not found.'},  404
        elif result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get stocks.'
            }, 500

        resp_list = {}
        for record in result:
            resp_list[record[1]] = [record[2], record[3]]

        return resp_list, 200

    async def handleGetAllTriggers(self):
        getBuyTriggers  = asyncio.create_task(self.handleGetAllBuyTriggers())
        getSellTriggers = asyncio.create_task(self.handleGetAllSellTriggers())
        
        buyTriggers, buyStatus = await getBuyTriggers
        sellTriggers, sellStatus = await getSellTriggers

        if buyStatus != 200:
            return {
                'errorMessage': 'Could not get buy triggers.'
            }, 500
        if sellStatus != 200:
            return {
                'errorMessage': 'Could not get sell triggers.'
            }, 500
        
        resp_list = {}
        for stock in buyTriggers.keys():
            resp_list[stock] = {'buy_triggers': buyTriggers[stock]}

        for stock in sellTriggers.keys():
            new_pair = {'sell_triggers': sellTriggers[stock]}
            if stock in resp_list:
                resp_list[stock].update(new_pair)
            resp_list[stock] = new_pair

        return resp_list, 200

    async def handleGetAllBuyTriggers(self):
        get_triggers_query = from_table_where_query.format(
            columns='*',
            table=buy_triggers_table,
            where=''
        )

        result = await self.fetchQuery(get_triggers_query)

        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get buy triggers.'
            }, 500

        resp_list = {}
        for record in result:
            stocks_list = {}
            if record[1] in resp_list:
                stocks_list = resp_list[record[1]]

            stocks_list[record[0]] = [record[2], record[3], record[4]]
            resp_list[record[1]] = stocks_list

        return resp_list, 200
        
    async def handleGetUserBuyTriggers(self, user_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404
        
        get_triggers_query = from_table_where_user_query.format(
            columns='*',
            table=buy_triggers_table,
            user=user_id
        )

        result = await self.fetchQuery(get_triggers_query)

        if result == []:
            return {'errorMessage':'Triggers not found.'}, 404
        elif result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get triggers.'
            }, 500

        resp_list = {}
        for record in result:
            resp_list[record[1]] = [record[2], record[3], record[4]]

        return resp_list, 200

    async def handleGetAllSellTriggers(self):
        get_triggers_query = from_table_where_query.format(
            columns='*',
            table=sell_triggers_table,
            where=''
        )

        result = await self.fetchQuery(get_triggers_query)

        if result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get sell triggers.'
            }, 404

        resp_list = {}
        for record in result:
            stocks_list = {}
            if record[1] in resp_list:
                stocks_list = resp_list[record[1]]

            stocks_list[record[0]] = [record[2], record[3], record[4]]
            resp_list[record[1]] = stocks_list

        return resp_list, 200

    async def handleGetUserSellTriggers(self, user_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        get_triggers_query = from_table_where_user_query.format(
            columns='*',
            table=sell_triggers_table,
            user=user_id
        )

        result = await self.fetchQuery(get_triggers_query)

        if result == []:
            return {'errorMessage':'Triggers not found.'}, 404
        elif result is None:
            return {
                'errorMessage': 'Unexpected error. Could not get triggers.'
            }, 500

        resp_list = {}
        for record in result:
            resp_list[record[1]] = [record[2], record[3], record[4]]

        return resp_list, 200

    async def handleAddFundsCommand(self, user_id, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            await self._addUser(user_id)

        error_resp = {'status': 'failure', 'message': 'Unexpected error. Could not add funds.'}
        success_resp = {'status': 'success', 'message': 'Funds successfully added.'}
        
        balances, status = await self.handleGetUserFundsCommand(user_id)

        if status != 200:
            return error_resp, status

        curr_funds = balances['available_funds']
        funds = Decimal(funds)

        add_funds_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance={f}'.format(f=funds + curr_funds),
            user=user_id)

        result = await self.executeQuery(add_funds_query)

        if type(result) != str:
            return error_resp, 500

        result = result.lower().split(' ')

        if len(result) == 2 and result[0] == 'update' and result[1] == '1':
            return success_resp, 200

        return error_resp, 500

    async def handleBuyStocksCommand(self, user_id, stock_id, stock_num, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        balances, status = await self.handleGetUserFundsCommand(user_id)

        if status != 200:
            return {'status':'failure', 'message':'Could not get user funds. Unexpected error.'}, status

        curr_funds = balances['available_funds']
        funds = Decimal(funds)

        stocks, status = await self.handleGetUserStocksCommand(user_id, stock_id)
        available_stock = 0
        reserved_stock = 0

        if stock_id in stocks: 
            available_stock = stocks[stock_id][0]
            reserved_stock = stocks[stock_id][1]

        if curr_funds < funds:
            return {
                'status': 'failure', 'message': 'Not enough funds in account.'
            }, 404

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
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully bought stocks.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to update user account.'
        }, 500

    async def handleSellStocksCommand(self, user_id, stock_id, stock_num, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        balances, status = await self.handleGetUserFundsCommand(user_id)
        
        if status != 200:
            return {'status':'failure', 'message':'Could not sell stocks. Unexpected error.'}, status
        
        curr_funds = balances['available_funds']
        funds = Decimal(funds)

        stocks, status = await self.handleGetUserStocksCommand(user_id, stock_id)
        available_stock = 0
        reserved_stock = 0

        if stock_id in stocks:
            available_stock = stocks[stock_id][0]
            reserved_stock = stocks[stock_id][1]

        if available_stock < stock_num:
            return {
                'status': 'failure', 'message': 'Not enough stocks in account.'
            }, 404

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
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully sold stocks.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to update user account.'
        }, 500

    async def handleBuyTriggerAmount(self, user_id, stock_id, amount):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        add_pending_trigger_query = "insert into {table} values ('{user}', '{stock}', {stock_amount}) on conflict (user_id, stock_id) do update" \
            " set stock_amount={stock_amount};".format(
                table=pending_buy_triggers_table,
                user=user_id,
                stock=stock_id,
                stock_amount=amount
            )

        result = await self.executeQuery(add_pending_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not set trigger amount.'
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully added trigger amount.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to set trigger amount.'
        }, 500

    async def handleBuyTriggerPrice(self, user_id, stock_id, price, transaction_num):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404
        
        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_amount_query = from_table_where_query.format(
            columns='*',
            table=pending_buy_triggers_table,
            where=where_clause
        )
        
        result = await self.fetchQuery(get_trigger_amount_query)

        if result == []:
            return {'status':'failure', 'message':'Trigger has no corresponding amount.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not set trigger price.'
            }, 500

        stock_amount = result[0][2]
        price = Decimal(price)
        amount_to_reserve = Decimal(stock_amount) * price

        balances, status = await self.handleGetUserFundsCommand(user_id)

        if status != 200:
            return {'status':'failure', 'message':'Could not get user funds. Unexpected error.'}, status

        curr_funds = balances['available_funds']

        if curr_funds < amount_to_reserve:
            return {'status':'failure', 'message':'Not enough funds in account to reserve.'}, 404
        
        set_buy_trigger_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance = account_balance - {res}, account_reserve = account_reserve + {res}'.format(
                res=amount_to_reserve
                ),
            user=user_id
        )
        set_buy_trigger_query = set_buy_trigger_query + \
            "delete from {table} where user_id = '{user}' AND stock_id = '{stock}';".format(
                table=pending_buy_triggers_table,
                user=user_id,
                stock=stock_id
            )
        set_buy_trigger_query = set_buy_trigger_query + \
            "insert into {table} values ('{user}', '{stock}', {stock_amount}, {stock_price}, {trans_num}) on conflict (user_id, stock_id) do update" \
            " set stock_amount={stock_amount}, stock_price={stock_price};".format(
                table=buy_triggers_table,
                user=user_id,
                stock=stock_id,
                stock_amount=stock_amount,
                stock_price=price,
                trans_num=transaction_num
            )

        _, cancelStatus = await self.handleCancelBuyTrigger(user_id, stock_id)
        result = await self.executeQuery(set_buy_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not set trigger price.'
            }, 500

        replacedTrigger = True if cancelStatus == 200 else False

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'user_id': user_id, 'stock_id': stock_id, 'stock_amount': stock_amount, 
                'price': price, 'transaction_num': transaction_num, 'replace': replacedTrigger
                }, 200

        return {
            'status': 'failure', 'message': 'Failed to set trigger price.'
        }, 500

    async def handleExecuteBuyTrigger(self, user_id, stock_id, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_query = from_table_where_query.format(
            columns='*',
            table=buy_triggers_table,
            where=where_clause
        )

        result = await self.fetchQuery(get_trigger_query)

        if result == []:
            return {'status':'failure', 'message':'There is no trigger to execute.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not execute trigger.'
            }, 500

        stock_amount = result[0][2]
        
        _, status = await self.handleCancelBuyTrigger(user_id, stock_id)
        
        if status != 200:
            return {
                'status':'failure', 'message':'Unexpected error. Could not release reserved funds.'
            }, 500

        buyResult, status = await self.handleBuyStocksCommand(user_id, stock_id, stock_amount, funds)
        
        if status != 200:
            return {
                'status':'failure', 'message': 'Could not purchase stocks.'
            }, 500
        
        return buyResult, status

    async def handleCancelBuyTrigger(self, user_id, stock_id, release_amount=0):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status':'failure', 'message': 'Specified user does not exist.'
            }, 404

        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_query = from_table_where_query.format(
            columns='*',
            table=buy_triggers_table,
            where=where_clause
        )

        result = await self.fetchQuery(get_trigger_query)

        if result == []:
            return {'status':'failure', 'message':'Cancel has no corresponding trigger.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not cancel trigger.'
            }, 500

        stock_amount = result[0][2]
        stock_price = result[0][3]
        reserved_amount = Decimal(stock_amount) * stock_price

        cancel_trigger_query = to_table_where_user_query.format(
            table=funds_table,
            fields='account_balance = account_balance + {res}, account_reserve = account_reserve - {res}'.format(
                res=reserved_amount,
                ),
            user=user_id
        )
        cancel_trigger_query = cancel_trigger_query + \
            "delete from {table} where user_id = '{user}' AND stock_id = '{stock}';".format(
                table=buy_triggers_table,
                user=user_id,
                stock=stock_id
            )

        result = await self.executeQuery(cancel_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not cancel trigger.'
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "delete 1" as our status string for the DELETE query
        if len(result) == 2 and result[0] == 'delete' and result[1] == '1':
            return {
                'status': 'success', 'message': 'Successfully cancelled trigger.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to cancel trigger.'
        }, 500

    async def handleSellTriggerAmount(self, user_id, stock_id, amount):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        add_pending_trigger_query = "insert into {table} values ('{user}', '{stock}', {stock_amount}) on conflict (user_id, stock_id) do update" \
            " set stock_amount={stock_amount};".format(
                table=pending_sell_triggers_table,
                user=user_id,
                stock=stock_id,
                stock_amount=amount
            )

        result = await self.executeQuery(add_pending_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not add trigger amount.'
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'status': 'success', 'message': 'Successfully added trigger amount.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to add trigger amount.'
        }, 500
        
    async def handleSellTriggerPrice(self, user_id, stock_id, price, transaction_num):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404
        
        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_amount_query = from_table_where_query.format(
            columns='*',
            table=pending_sell_triggers_table,
            where=where_clause
        )
        
        result = await self.fetchQuery(get_trigger_amount_query)

        if result == []:
            return {'status':'failure', 'message':'Trigger has no corresponding amount.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not set trigger price.'
            }, 500

        stock_amount = result[0][2]
        price = Decimal(price)
        amount_to_reserve = stock_amount

        balances, status = await self.handleGetUserStocksCommand(user_id, stock_id)

        if stock_id not in balances:
            return {'status':'failure', 'message':'No stocks in account of the given type.'}, 404
        elif status != 200:
            return {'status':'failure', 'message':'Could not get user stocks. Unexpected error.'}, status

        curr_stocks = balances[stock_id][0]

        if curr_stocks < amount_to_reserve:
            return {'status':'failure', 'message':'Not enough stocks in account to reserve.'}, 404
        
        set_sell_trigger_query = to_table_where_query.format(
            table=stocks_table,
            fields='stock_balance = stock_balance - {res}, stock_reserve = stock_reserve + {res}'.format(
                res=amount_to_reserve
                ),
            where=where_clause
        )
        set_sell_trigger_query = set_sell_trigger_query + \
            "delete from {table} where user_id = '{user}' AND stock_id = '{stock}';".format(
                table=pending_sell_triggers_table,
                user=user_id,
                stock=stock_id
            )
        set_sell_trigger_query = set_sell_trigger_query + \
            "insert into {table} values ('{user}', '{stock}', {stock_amount}, {stock_price}, {trans_num}) on conflict (user_id, stock_id) do update" \
            " set stock_amount={stock_amount}, stock_price={stock_price};".format(
                table=sell_triggers_table,
                user=user_id,
                stock=stock_id,
                stock_amount=stock_amount,
                stock_price=price,
                trans_num=transaction_num
            )

        _, cancelStatus = await self.handleCancelSellTrigger(user_id, stock_id)
        result = await self.executeQuery(set_sell_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not set trigger price.'
            }, 500

        replacedTrigger = True if cancelStatus == 200 else False

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        if len(result) == 3 and result[0] == 'insert' and result[2] == '1':
            return {
                'user_id': user_id, 'stock_id': stock_id, 'stock_amount': stock_amount, 
                'price': price, 'transaction_num': transaction_num, 'replace': replacedTrigger
                }, 200

        return {
            'status': 'failure', 'message': 'Failed to set trigger price.'
        }, 500

    async def handleExecuteSellTrigger(self, user_id, stock_id, funds):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_query = from_table_where_query.format(
            columns='*',
            table=sell_triggers_table,
            where=where_clause
        )

        result = await self.fetchQuery(get_trigger_query)

        if result == []:
            return {'status':'failure', 'message':'There is no trigger to execute.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not execute trigger.'
            }, 500

        stock_amount = result[0][2]
        
        _, status = await self.handleCancelSellTrigger(user_id, stock_id)
        
        if status != 200:
            return {
                'status':'failure', 'message':'Unexpected error. Could not release reserved stocks.'
            }, 500

        sellResult, status = await self.handleSellStocksCommand(user_id, stock_id, stock_amount, funds)
        
        if status != 200:
            return {
                'status':'failure', 'message': 'Could not sell stocks.'
            }, 500
        
        return sellResult, status

    async def handleCancelSellTrigger(self, user_id, stock_id):
        user_exists = await self._checkUserExists(user_id)

        if not user_exists:
            return {
                'status': 'failure', 'message': 'Specified user does not exist.'
            }, 404

        where_clause = "where user_id='{user}' AND stock_id='{stock}'".format(user=user_id, stock=stock_id)

        get_trigger_query = from_table_where_query.format(
            columns='*',
            table=sell_triggers_table,
            where=where_clause
        )

        result = await self.fetchQuery(get_trigger_query)

        if result == []:
            return {'status':'failure', 'message':'Cancel has no corresponding trigger.'}, 404
        elif result is None:
            return {
                'status':'failure', 'message': 'Unexpected error. Could not cancel trigger.'
            }, 500

        stock_amount = result[0][2]
        reserved_amount = stock_amount

        cancel_trigger_query = to_table_where_query.format(
            table=stocks_table,
            fields='stock_balance = stock_balance + {res}, stock_reserve = stock_reserve - {res}'.format(
                res=reserved_amount,
                ),
            where=where_clause
        )
        cancel_trigger_query = cancel_trigger_query + \
            "delete from {table} where user_id = '{user}' AND stock_id = '{stock}';".format(
                table=sell_triggers_table,
                user=user_id,
                stock=stock_id
            )

        result = await self.executeQuery(cancel_trigger_query)

        if type(result) != str:
            return {
                'status': 'failure', 'message': 'Could not cancel trigger.'
            }, 500

        result = result.lower().split(' ')
        # Checks we get back "delete 1" as our status string for the DELETE query
        if len(result) == 2 and result[0] == 'delete' and result[1] == '1':
            return {
                'status': 'success', 'message': 'Successfully cancelled trigger.'
            }, 200

        return {
            'status': 'failure', 'message': 'Failed to cancel trigger.'
        }, 500

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
            balance=Decimal(0),
            reserve=Decimal(0))
        result = await self.executeQuery(add_user_query)

        if type(result) != str:
            return False

        result = result.lower().split(' ')
        # Checks we get back "insert <some_num> 1" as our status string for the INSERT query
        return len(result) == 3 and result[0] == 'insert' and result[2] == '1'
