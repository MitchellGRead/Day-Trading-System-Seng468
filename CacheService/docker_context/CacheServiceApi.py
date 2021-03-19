from sanic import Sanic, response
from sanic.log import logger

import config
import endpoints
import apiListeners
from cacheInputSchema import *

app = Sanic(config.CACHE_SERVER_NAME)
app.config['KEEP_ALIVE_TIMEOUT'] = 10


# GET ENDPOINTS -----------------------------------------------

# Get the user's funds
@app.route(endpoints.get_user_funds_endpoint, methods=['GET'])
async def getUserFunds(request, user_id):
    result, status = await app.config['serviceLogic'].getUserFunds(user_id)
    return response.json(result, status=status)


# Get the user's stocks
@app.route(endpoints.get_user_stocks_endpoint, methods=['GET'])
async def getUserStocks(request, user_id, stock_id):
    if stock_id:
        res, err = validateRequest(stock_id, one_to_three_letter_string)
        if not res:
            return response.json(errorResult(err, stock_id), status=400)

    result, status = await app.config['serviceLogic'].getUserStocks(user_id, stock_id)
    return response.json(result, status=status)


# Gets a quote price
@app.route(endpoints.get_quote_endpoint, methods=['GET'])
async def getQuote(request, user_id, stock_id, trans_num):
    if stock_id:
        res, err = validateRequest(stock_id, one_to_three_letter_string)
        if not res:
            return response.json(errorResult(err, stock_id), status=400)

    result, status = await app.config['serviceLogic'].getQuote(trans_num, user_id, stock_id)
    return response.json(result, status=status)


@app.route(endpoints.get_bulk_quotes_endpoint, methods=['GET'])
async def getBulkQuote(request):
    user_ids = request.args.getlist('user_id', '')
    stock_ids = request.args.getlist('stock_id', '')
    transaction_nums = request.args.getlist('transaction_num', '')

    if isinstance(user_ids, list) & isinstance(stock_ids, list) & isinstance(transaction_nums, list):
        if len(user_ids) == len(stock_ids) == len(transaction_nums):
            result, status = await app.config['serviceLogic'].getBulkQuote(user_ids, stock_ids, transaction_nums)
            return response.json(result, status=status)
        else:
            return response.json(errorResult("error: mismatched list lengths", data=''), status=400)
    else:
        return response.json(errorResult("error: not all lists", data=''), status=400)


# Get active buy command
@app.route(endpoints.get_buy_endpoint, methods=['GET'])
async def getBuyStocks(request, user_id):
    result, status = await app.config['serviceLogic'].getBuyStocks(user_id)
    return response.json(result, status=status)


# Get active sell command
@app.route(endpoints.get_sell_endpoint, methods=['GET'])
async def getSellStocks(request, user_id):
    result, status = await app.config['serviceLogic'].getSellStocks(user_id)
    return response.json(result, status=status)


# POST ENDPOINTS -----------------------------------------------


# Add funds to user's account
@app.route(endpoints.add_funds_endpoint, methods=['POST'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].addFunds(data)
    return response.json(result, status=status)


# Remove funds from user's account
# @app.route(endpoints.remove_funds_endpoint, methods=['POST'])
async def removeFunds(request):
    res, err = validateRequest(request.json, remove_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    # TODO: Decide if this method should be supported
    return None


# Buy stocks endpoint -- removes funds and adds stocks
@app.route(endpoints.buy_stocks_endpoint, methods=['POST'])
async def buyStocks(request):
    res, err = validateRequest(request.json, buy_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].buyStocks(data)
    return response.json(result, status=status)


# Sell stocks endpoint -- add funds and removes stocks
@app.route(endpoints.sell_stocks_endpoint, methods=['POST'])
async def sellStocks(request):
    res, err = validateRequest(request.json, sell_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].sellStocks(data)
    return response.json(result, status=status)


# Get active buy command
@app.route(endpoints.commit_buy_endpoint, methods=['POST'])
async def commitBuyStocks(request):
    res, err = validateRequest(request.json, user_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].commitBuyStocks(data)
    return response.json(result, status=status)


# Get active buy command
@app.route(endpoints.commit_sell_endpoint, methods=['POST'])
async def commitSellStocks(request):
    res, err = validateRequest(request.json, user_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].commitSellStocks(data)
    return response.json(result, status=status)


# Get active buy command
@app.route(endpoints.cancel_buy_endpoint, methods=['POST'])
async def cancelBuy(request):
    res, err = validateRequest(request.json, user_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].cancelBuy(data)
    return response.json(result, status=status)


# Get active buy command
@app.route(endpoints.cancel_sell_endpoint, methods=['POST'])
async def cancelSell(request):
    res, err = validateRequest(request.json, user_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].cancelSell(data)
    return response.json(result, status=status)


@app.route(endpoints.update_user_cache, methods=['POST'])
async def updateUserCache(request):
    res, err = validateRequest(request.json, update_user_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].updateUserCache(data['user_id'])
    return response.json(result, status=status)


@app.route(endpoints.update_stock_cache, methods=['POST'])
async def updateUserCache(request):
    res, err = validateRequest(request.json, update_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['serviceLogic'].updateStockCache(data['user_id'], data['stock_id'])
    return response.json(result, status=status)

# DB SERVICE INITIALIZATION -----------------------------------------------


if __name__ == "__main__":
    # Before app start
    app.register_listener(apiListeners.connectRedis, 'before_server_start')
    app.register_listener(apiListeners.initRedisHandler, 'before_server_start')
    app.register_listener(apiListeners.initAuditHandler, 'before_server_start')
    app.register_listener(apiListeners.initLegacyStockHandler, 'before_server_start')
    app.register_listener(apiListeners.initCacheHandler, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')

    # Before app stop
    app.register_listener(apiListeners.closeRedis, 'before_server_stop')
    app.register_listener(apiListeners.closeHandlerClients, 'before_server_stop')

    app.run(
        host=config.CACHE_SERVER_IP,
        port=config.CACHE_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.ACCESS_LOGS,
        auto_reload=True,
        workers=config.CACHE_SERVICE_WORKERS
    )
