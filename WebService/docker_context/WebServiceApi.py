
from sanic import Sanic, response

import config
import endpoints
import apiListeners
from clientInputSchema import *

app = Sanic(config.WEB_SERVER_NAME)


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

    await app.config['logic'].handleQuote(data)
    return response.json(data)


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

    await app.config['logic'].handleDisplaySummary(data)
    return response.json(data)


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

    await app.config['logic'].handleDumplog(data)
    return response.json(data)


@app.route(endpoints.add_funds_endpoint, methods=['POST'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleAdd(data)
    return response.json(data)


# BUY ENDPOINTS ------------------------------------------------
@app.route(endpoints.buy_endpoint, methods=['POST'])
async def buyStock(request):
    res, err = validateRequest(request.json, buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleBuy(data)
    return response.json(data)


@app.route(endpoints.commit_buy_endpoint, methods=['POST'])
async def commitBuy(request):
    res, err = validateRequest(request.json, commit_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCommitBuy(data)
    return response.json(data)


@app.route(endpoints.cancel_buy_endpoint, methods=['POST'])
async def cancelBuy(request):
    res, err = validateRequest(request.json, cancel_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCancelBuy(data)
    return response.json(data)

# --------------------------------------------------------------


# BUY TRIGGER ENDPOINTS ----------------------------------------
@app.route(endpoints.set_buy_amount_endpoint, methods=['POST'])
async def setBuyAmount(request):
    res, err = validateRequest(request.json, set_buy_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleBuyAmount(data)
    return response.json(data)


@app.route(endpoints.set_buy_trigger_endpoint, methods=['POST'])
async def setBuyTrigger(request):
    res, err = validateRequest(request.json, set_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleBuyTrigger(data)
    return response.json(data)


@app.route(endpoints.cancel_set_buy_endpoint, methods=['POST'])
async def cancelBuyTrigger(request):
    res, err = validateRequest(request.json, cancel_set_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCancelBuyTrigger(data)
    return response.json(data)
# --------------------------------------------------------------


# SELL ENDPOINTS -----------------------------------------------
@app.route(endpoints.sell_endpoint, methods=['POST'])
async def sellStock(request):
    res, err = validateRequest(request.json, sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleSell(data)
    return response.json(data)


@app.route(endpoints.commit_sell_endpoint, methods=['POST'])
async def commitSell(request):
    res, err = validateRequest(request.json, commit_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCommitSell(data)
    return response.json(data)


@app.route(endpoints.cancel_sell_endpoint, methods=['POST'])
async def cancelSell(request):
    res, err = validateRequest(request.json, cancel_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCancelSell(data)
    return response.json(data)

# --------------------------------------------------------------


# SELL TRIGGER ENDPOINTS ---------------------------------------
@app.route(endpoints.set_sell_amount_endpoint, methods=['POST'])
async def setSellAmount(request):
    res, err = validateRequest(request.json, set_sell_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleSellAmount(data)
    return response.json(data)


@app.route(endpoints.set_sell_trigger_endpoint, methods=['POST'])
async def setSellTrigger(request):
    res, err = validateRequest(request.json, set_sell_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleSellTrigger(data)
    return response.json(data)


@app.route(endpoints.cancel_set_sell_endpoint, methods=['POST'])
async def cancelSellTrigger(request):
    res, err = validateRequest(request.json, cancel_set_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    await app.config['logic'].handleCancelSellTrigger(data)
    return response.json(data)
# --------------------------------------------------------------


if __name__ == '__main__':
    app.register_listener(apiListeners.initClient, 'before_server_start')
    app.register_listener(apiListeners.initAudit, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')

    app.register_listener(apiListeners.closeClient, 'before_server_stop')

    app.run(
        host=config.WEB_SERVER_IP,
        port=config.WEB_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.ACCESS_LOGS,
        auto_reload=True,
        workers=config.WEB_SERVER_WORKERS
    )
