from sanic import Sanic, response

import config
from transactionInputSchema import *
import endpoints
import apiListeners

app = Sanic(config.TRANSACTION_SERVER_NAME)


@app.route(endpoints.quote_endpoint, methods=['GET'])
async def getQuote(request):
    data = request.json
    res, err = validateRequest(data, quote_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].getQuote(data['trans_num'], data['user_id'], data['stock_symbol'])

    # Format RETURNS for all commands

    return response.json(data)


# BUY ENDPOINTS ------------------------------------------------
@app.route(endpoints.buy_endpoint, methods=['POST'])
async def buyStock(request):
    data = request.json
    res, err = validateRequest(data, buy_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].buyStock(data['trans_num'], data['user_id'], data['stock_symbol'], data['amount'])

    return response.json(data)


@app.route(endpoints.commit_buy_endpoint, methods=['POST'])
async def commitBuy(request):
    data = request.json
    res, err = validateRequest(data, commit_buy_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].commitBuy(data['trans_num'], data['user_id'])

    return response.json(data)


@app.route(endpoints.cancel_buy_endpoint, methods=['POST'])
async def cancelBuy(request):
    data = request.json
    res, err = validateRequest(data, cancel_buy_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].cancelBuy(data['trans_num'], data['user_id'])

    return response.json(data)
# --------------------------------------------------------------


# SELL ENDPOINTS ------------------------------------------------
@app.route(endpoints.sell_endpoint, methods=['POST'])
async def sellStock(request):
    data = request.json
    res, err = validateRequest(data, sell_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].sellStock(data['trans_num'], data['user_id'],
                                                data['stock_symbol'], data['amount'])

    return response.json(data)


@app.route(endpoints.commit_sell_endpoint, methods=['POST'])
async def commitSell(request):
    data = request.json
    res, err = validateRequest(data, commit_sell_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].commitSell(data['trans_num'], data['user_id'])

    return response.json(data)


@app.route(endpoints.cancel_sell_endpoint, methods=['POST'])
async def cancelSell(request):
    data = request.json
    res, err = validateRequest(data, cancel_sell_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    data = app.config['serviceLogic'].cancelSell(data['trans_num'], data['user_id'])

    return response.json(data)
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
    app.register_listener(apiListeners.connectRedis, 'before_server_start')
    app.register_listener(apiListeners.initRedisHandler, 'before_server_start')
    app.register_listener(apiListeners.initAudit, 'before_server_start')
    app.register_listener(apiListeners.initLegacyStock, 'before_server_start')
    app.register_listener(apiListeners.initBaseLogic, 'before_server_start')

    app.register_listener(apiListeners.closeClient, 'before_server_stop')
    app.register_listener(apiListeners.closeRedis, 'before_server_stop')

    app.run(
        host=config.TRANSACTION_SERVER_IP,
        port=config.TRANSACTION_SERVER_PORT,
        debug=config.RUN_DEBUG,
        auto_reload=True
    )
