from sanic import Sanic, response

import config
import endpoints
import apiListeners
from clientInputSchema import *

app = Sanic(config.DATABASE_SERVER_NAME)

#TODO: Change the PSQL datatype for the account balance -- it cannot accomodate large numbers

# GET ENDPOINTS -----------------------------------------------

# Get all users' funds
@app.route(endpoints.get_all_funds_endpoint, methods=['GET'])
async def getAllFunds(request):
    result, status = await app.config['logic'].handleGetAllFundsCommand()
    return response.json(result, status=status)


# Get the user's funds
@app.route(endpoints.get_user_funds_endpoint, methods=['GET'])
async def getUserFunds(request, user_id):
    result, status = await app.config['logic'].handleGetFundsCommand(user_id)
    return response.json(result, status=status)


#Get all users' stocks
@app.route(endpoints.get_all_stocks_endpoint, methods=['GET'])
async def getAllStocks(request):
    result, status = await app.config['logic'].handleGetAllStocksCommand()
    return response.json(result, status=status)


# Get the user's stocks
@app.route(endpoints.get_user_stocks_endpoint, methods=['GET'])
async def getUserStocks(request, user_id):
    stock_id = request.args.get('stock_id', '')

    if stock_id:
        res, err = validateRequest(stock_id, one_to_three_letter_string)
        if not res:
            return response.json(errorResult(err, stock_id), status=400)

    result, status = await app.config['logic'].handleGetStocksCommand(user_id, stock_id)
    return response.json(result, status=status)


# Get all buy triggers
@app.route(endpoints.get_all_buy_triggers_endpoint, methods=['GET'])
async def getAllBuyTriggers(request):
    result, status = await app.config['logic'].handleGetAllBuyTriggers()
    return response.json(result, status=status)


# Get the user's buy triggers
@app.route(endpoints.get_user_buy_triggers_endpoint, methods=['GET'])
async def getUserBuyTriggers(request, user_id):
    result, status = await app.config['logic'].handleGetUserBuyTriggers(user_id)
    return response.json(result, status=status)


# Get all sell triggers
@app.route(endpoints.get_all_sell_triggers_endpoint, methods=['GET'])
async def getAllSellTriggers(request):
    result, status = await app.config['logic'].handleGetAllSellTriggers()
    return response.json(result, status=status)


# Get the user's sell triggers
@app.route(endpoints.get_user_sell_triggers_endpoint, methods=['GET'])
async def getUserSellTriggers(request, user_id):
    result, status = await app.config['logic'].handleGetUserSellTriggers(user_id)
    return response.json(result, status=status)


# Get the system's summary
@app.route(endpoints.get_summary_endpoint, methods=['GET'])
async def getSummary(request, user_id):
    result, status = await app.config['logic'].handleGetSummaryCommand(user_id)
    return response.json(result, status=status)


# POST ENDPOINTS -----------------------------------------------


# Add funds to user's account
@app.route(endpoints.add_funds_endpoint, methods=['POST'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    
    data = request.json 
    result, status = await app.config['logic'].handleAddFundsCommand(data['user_id'], data['funds'])
    return response.json(result, status=status)


# Remove funds from user's account
# @app.route(endpoints.remove_funds_endpoint, methods=['POST'])
async def removeFunds(request):
    res, err = validateRequest(request.json, remove_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
 
    #TODO: Decide if this method should be supported
    return None


# Buy stocks endpoint -- removes funds and adds stocks
@app.route(endpoints.buy_stocks_endpoint, methods=['POST'])
async def buyStocks(request):
    res, err = validateRequest(request.json, buy_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleBuyStocksCommand(data['user_id'], data['stock_symbol'], data['stock_amount'], data['funds'])
    return response.json(result, status=status)


# Sell stocks endpoint -- add funds and removes stocks
@app.route(endpoints.sell_stocks_endpoint, methods=['POST'])
async def sellStocks(request):
    res, err = validateRequest(request.json, sell_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleSellStocksCommand(data['user_id'], data['stock_symbol'], data['stock_amount'], data['funds'])
    return response.json(result, status=status)


# Set buy trigger amount endpoint -- set the amount of stock to buy
@app.route(endpoints.set_buy_trigger_amount_endpoint, methods=['POST'])
async def setBuyTriggerAmount(request):
    res, err = validateRequest(request.json, buy_trigger_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    
    data = request.json
    result, status = await app.config['logic'].handleBuyTriggerAmount(data['user_id'], data['stock_symbol'], data['amount'])
    return response.json(result, status=status)


# Set buy trigger price endpoint -- set the price at which to buy
@app.route(endpoints.set_buy_trigger_price_endpoint, methods=['POST'])
async def setBuyTriggerPrice(request):
    res, err = validateRequest(request.json, buy_trigger_price_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleBuyTriggerPrice(data['user_id'], data['stock_symbol'], data['price'], data['transaction_num'])
    return response.json(result, status=status)


# Execute buy trigger endpoint -- execute the specified trigger
@app.route(endpoints.execute_buy_trigger_endpoint, methods=['POST'])
async def executeBuyTrigger(request):
    res, err = validateRequest(request.json, execute_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleExecuteBuyTrigger(data['user_id'], data['stock_symbol'], data['funds'])
    return response.json(result, status=status)


# Cancel buy trigger endpoint -- cancel the specified trigger
@app.route(endpoints.cancel_set_buy_endpoint, methods=['POST'])
async def cancelBuyTrigger(request):
    res, err = validateRequest(request.json, cancel_set_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleCancelBuyTrigger(data['user_id'], data['stock_symbol'])
    return response.json(result, status=status)


# Set sell trigger amount endpoint -- set the amount of stock to sell
@app.route(endpoints.set_sell_trigger_amount_endpoint, methods=['POST'])
async def setSellTriggerAmount(request):
    res, err = validateRequest(request.json, sell_trigger_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleSellTriggerAmount(data['user_id'], data['stock_symbol'], data['amount'])
    return response.json(result, status=status)


# Set sell trigger price endpoint -- set the price at which to sell
@app.route(endpoints.set_sell_trigger_price_endpoint, methods=['POST'])
async def setSellTriggerPrice(request):
    res, err = validateRequest(request.json, sell_trigger_price_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleSellTriggerPrice(data['user_id'], data['stock_symbol'], data['price'], data['transaction_num'])
    return response.json(result, status=status)


# Execute sell trigger endpoint -- execute the specified trigger
@app.route(endpoints.execute_sell_trigger_endpoint, methods=['POST'])
async def executeSellTrigger(request):
    res, err = validateRequest(request.json, execute_sell_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleExecuteSellTrigger(data['user_id'], data['stock_symbol'], data['funds'])
    return response.json(result, status=status)


# Cancel sell trigger endpoint -- cancel the specified trigger
@app.route(endpoints.cancel_set_sell_endpoint, methods=['POST'])
async def cancelSellTrigger(request):
    res, err = validateRequest(request.json, cancel_set_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result, status = await app.config['logic'].handleCancelSellTrigger(data['user_id'], data['stock_symbol'])
    return response.json(result, status=status)


# DB SERVICE INITIALIZATION -----------------------------------------------


if __name__ == "__main__":
    
    # Before app start
    app.register_listener(apiListeners.initDbConnections, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')
    # Before app stop
    app.register_listener(apiListeners.closeDbConnections, 'before_server_stop')

    app.run(
        host=config.DATABASE_SERVER_IP,
        port=config.DATABASE_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.ACCESS_LOGS,
        auto_reload=True,
        workers=config.DATABASE_SERVICE_WORKERS
    )
