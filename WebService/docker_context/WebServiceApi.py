
from sanic import Sanic, response
from sanic.log import logger

import config
import endpoints
import apiListeners
from clientInputSchema import *

app = Sanic(config.WEB_SERVER_NAME)
app.config['KEEP_ALIVE_TIMEOUT'] = 10


@app.route(endpoints.quote_endpoint, methods=['GET'])
async def getQuote(request, command, trans_num, user_id, stock_symbol):
    data = {
        'command': command,
        'transaction_num': trans_num,
        'user_id': user_id,
        'stock_symbol': stock_symbol
    }
    res, err = validateRequest(data, quote_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    resp, status = await app.config['logic'].handleQuote(data)
    return response.json(resp, status=status)


@app.route(endpoints.display_summary_endpoint, methods=['GET'])
async def getAccountSummary(request, command, trans_num, user_id):
    data = {
        'command': command,
        'transaction_num': trans_num,
        'user_id': user_id
    }
    res, err = validateRequest(data, display_summary_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    resp, status = await app.config['logic'].handleDisplaySummary(data)
    return response.json(resp, status=status)


@app.route(endpoints.dumplog_endpoint, methods=['GET'])
async def createDumplog(request, command, trans_num, filename):
    user_id = request.args.get('user_id', '')
    data = {
        'command': command,
        'transaction_num': trans_num,
        'filename': filename,
    }
    if user_id:
        data['user_id'] = user_id

    res, err = validateRequest(data, dumplog_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    # TODO change so this sends a file
    await app.config['logic'].handleDumplog(data)
    # TODO if status != 200 then return json object else return file
    return response.json(data)


@app.route(endpoints.add_funds_endpoint, methods=['POST', 'OPTIONS'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleAdd(data)
    return response.json(resp, status=status)


# BUY ENDPOINTS ------------------------------------------------
@app.route(endpoints.buy_endpoint, methods=['POST', 'OPTIONS'])
async def buyStock(request):
    res, err = validateRequest(request.json, buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleBuy(data)
    return response.json(resp, status=status)


@app.route(endpoints.commit_buy_endpoint, methods=['POST', 'OPTIONS'])
async def commitBuy(request):
    res, err = validateRequest(request.json, commit_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCommitBuy(data)
    return response.json(resp, status=status)


@app.route(endpoints.cancel_buy_endpoint, methods=['POST', 'OPTIONS'])
async def cancelBuy(request):
    res, err = validateRequest(request.json, cancel_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCancelBuy(data)
    return response.json(resp, status=status)

# --------------------------------------------------------------


# BUY TRIGGER ENDPOINTS ----------------------------------------
@app.route(endpoints.set_buy_amount_endpoint, methods=['POST', 'OPTIONS'])
async def setBuyAmount(request):
    res, err = validateRequest(request.json, set_buy_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleBuyAmount(data)
    return response.json(resp, status=status)


@app.route(endpoints.set_buy_trigger_endpoint, methods=['POST', 'OPTIONS'])
async def setBuyTrigger(request):
    res, err = validateRequest(request.json, set_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleBuyTrigger(data)
    return response.json(resp, status=status)


@app.route(endpoints.cancel_set_buy_endpoint, methods=['POST', 'OPTIONS'])
async def cancelBuyTrigger(request):
    res, err = validateRequest(request.json, cancel_set_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCancelBuyTrigger(data)
    return response.json(resp, status=status)
# --------------------------------------------------------------


# SELL ENDPOINTS -----------------------------------------------
@app.route(endpoints.sell_endpoint, methods=['POST', 'OPTIONS'])
async def sellStock(request):
    res, err = validateRequest(request.json, sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleSell(data)
    return response.json(resp, status=status)


@app.route(endpoints.commit_sell_endpoint, methods=['POST', 'OPTIONS'])
async def commitSell(request):
    res, err = validateRequest(request.json, commit_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCommitSell(data)
    return response.json(resp, status=status)


@app.route(endpoints.cancel_sell_endpoint, methods=['POST', 'OPTIONS'])
async def cancelSell(request):
    res, err = validateRequest(request.json, cancel_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCancelSell(data)
    return response.json(resp, status=status)

# --------------------------------------------------------------


# SELL TRIGGER ENDPOINTS ---------------------------------------
@app.route(endpoints.set_sell_amount_endpoint, methods=['POST', 'OPTIONS'])
async def setSellAmount(request):
    res, err = validateRequest(request.json, set_sell_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleSellAmount(data)
    return response.json(resp, status=status)


@app.route(endpoints.set_sell_trigger_endpoint, methods=['POST', 'OPTIONS'])
async def setSellTrigger(request):
    res, err = validateRequest(request.json, set_sell_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleSellTrigger(data)
    return response.json(resp, status=status)


@app.route(endpoints.cancel_set_sell_endpoint, methods=['POST', 'OPTIONS'])
async def cancelSellTrigger(request):
    res, err = validateRequest(request.json, cancel_set_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    resp, status = await app.config['logic'].handleCancelSellTrigger(data)
    return response.json(resp, status=status)
# --------------------------------------------------------------

@app.middleware('response')
async def enableResponseCORS(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'

@app.middleware('request')
async def allowCORSOptions(request):
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    if request.method == 'OPTIONS':
        return response.json({}, headers=cors_headers)


if __name__ == '__main__':
    app.register_listener(apiListeners.initAudit, 'before_server_start')
    app.register_listener(apiListeners.initTransaction, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')

    app.register_listener(apiListeners.closeHandlerClients, 'before_server_stop')

    app.run(
        host=config.WEB_SERVER_IP,
        port=config.WEB_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.ACCESS_LOGS,
        auto_reload=True,
        workers=config.WEB_SERVER_WORKERS
    )
