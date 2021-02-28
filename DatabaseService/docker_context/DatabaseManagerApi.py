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
    result = await app.config['logic'].handleGetAllFundsCommand()
    return response.json(result)


# Get the user's funds
@app.route(endpoints.get_user_funds_endpoint, methods=['GET'])
async def getUserFunds(request, user_id):
    result = await app.config['logic'].handleGetFundsCommand(user_id)
    return response.json(result)


#Get all users' stocks
@app.route(endpoints.get_all_stocks_endpoint, methods=['GET'])
async def getAllStocks(request):
    result = await app.config['logic'].handleGetAllStocksCommand()
    return response.json(result)


# Get the user's stocks
@app.route(endpoints.get_user_stocks_endpoint, methods=['GET'])
async def getUserStocks(request, user_id):
    stock_id = request.args.get('stock_id', '')

    if stock_id:
        res, err = validateRequest(stock_id, one_to_three_letter_string)
        if not res:
            return response.json(errorResult(err, stock_id), status=400)

    result = await app.config['logic'].handleGetStocksCommand(user_id, stock_id)
    return response.json(result)


# Get the system's summary
@app.route(endpoints.get_summary_endpoint, methods=['GET'])
async def getSummary(request, user_id):
    result = await app.config['logic'].handleGetSummaryCommand(user_id)
    return response.json(result)


# POST ENDPOINTS -----------------------------------------------


# Add funds to user's account
@app.route(endpoints.add_funds_endpoint, methods=['POST'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    
    data = request.json 
    result = await app.config['logic'].handleAddFundsCommand(data['user_id'], data['funds'])
    return response.json(result)


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
    result = await app.config['logic'].handleBuyStocksCommand(data['user_id'], data['stock_symbol'], data['stock_amount'], data['funds'])
    return response.json(result)


# Sell stocks endpoint -- add funds and removes stocks
@app.route(endpoints.sell_stocks_endpoint, methods=['POST'])
async def sellStocks(request):
    res, err = validateRequest(request.json, sell_stock_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    result = await app.config['logic'].handleSellStocksCommand(data['user_id'], data['stock_symbol'], data['stock_amount'], data['funds'])
    return response.json(result)


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
        access_log=config.RUN_DEBUG,
        auto_reload=True,
        workers=config.DATABASE_SERVICE_WORKERS
    )
