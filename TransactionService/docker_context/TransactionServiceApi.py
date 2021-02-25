from sanic import Sanic, response

import config
from transactionInputSchema import *
import endpoints
import apiListeners

app = Sanic(config.TRANSACTION_SERVER_NAME)


@app.route(endpoints.quote_endpoint, methods=['GET'])
async def getQuote(request, trans_num, user_id, stock_symbol):
    data = {
        'transaction_num': trans_num,
        'user_id': user_id,
        'stock_symbol': stock_symbol
    }
    res, err = validateRequest(data, quote_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    resp = await app.config['serviceLogic'].getQuote(data['trans_num'], data['user_id'], data['stock_symbol'])

    return resp


@app.route(endpoints.add_funds_endpoint, methods=['POST'])
async def addFunds(request):
    res, err = validateRequest(request.json, add_funds_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].addFunds(data['trans_num'], data['user_id'], data['amount'])

    return resp


# BUY ENDPOINTS ------------------------------------------------
@app.route(endpoints.buy_endpoint, methods=['POST'])
async def buyStock(request):
    res, err = validateRequest(request.json, buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].buyStock(data['trans_num'], data['user_id'], data['stock_symbol'],
                                                     data['amount'])

    return resp


@app.route(endpoints.commit_buy_endpoint, methods=['POST'])
async def commitBuy(request):
    res, err = validateRequest(request.json, commit_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].commitBuy(data['trans_num'], data['user_id'])

    return resp


@app.route(endpoints.cancel_buy_endpoint, methods=['POST'])
async def cancelBuy(request):
    res, err = validateRequest(request.json, cancel_buy_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].cancelBuy(data['trans_num'], data['user_id'])

    return resp


# --------------------------------------------------------------


# SELL ENDPOINTS ------------------------------------------------
@app.route(endpoints.sell_endpoint, methods=['POST'])
async def sellStock(request):
    res, err = validateRequest(request.json, sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].sellStock(data['trans_num'], data['user_id'],
                                                      data['stock_symbol'], data['amount'])

    return resp


@app.route(endpoints.commit_sell_endpoint, methods=['POST'])
async def commitSell(request):
    res, err = validateRequest(request.json, commit_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].commitSell(data['trans_num'], data['user_id'])

    return resp


@app.route(endpoints.cancel_sell_endpoint, methods=['POST'])
async def cancelSell(request):
    res, err = validateRequest(request.json, cancel_sell_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)
    data = request.json

    resp = await app.config['serviceLogic'].cancelSell(data['trans_num'], data['user_id'])

    return resp


# --------------------------------------------------------------


async def postRequest(url, data):
    client = app.config['client']
    async with client.post(url, json=data) as resp:
        js = await resp.json()
        return js


async def getRequest(self, url, params=None):
    async with self.client.get(url, params=params) as resp:
        js = await resp.json()
        return js


if __name__ == '__main__':
    app.register_listener(apiListeners.initClient, 'before_server_start')
    app.register_listener(apiListeners.initAudit, 'before_server_start')
    app.register_listener(apiListeners.initTransactionLogic, 'before_server_start')

    app.register_listener(apiListeners.closeClient, 'before_server_stop')

    app.run(
        host=config.TRANSACTION_SERVER_IP,
        port=config.TRANSACTION_SERVER_PORT,
        debug=config.RUN_DEBUG,
        auto_reload=True
    )
