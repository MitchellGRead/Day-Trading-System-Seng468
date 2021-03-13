
from sanic import Sanic, response

import config
from triggerInputSchema import *
import endpoints
import apiListeners

app = Sanic(config.TRIGGER_SERVER_NAME)


# BUY TRIGGER ENDPOINTS ----------------------------------------
@app.route(endpoints.buy_amount_endpoint, methods=['POST'])
async def setBuyAmount(request):
    res, err = validateRequest(request.json, set_buy_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)


@app.route(endpoints.buy_trigger_endpoint, methods=['POST'])
async def setBuyTrigger(request):
    res, err = validateRequest(request.json, set_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)


@app.route(endpoints.cancel_buy_trigger_endpoint, methods=['POST'])
async def cancelBuyTrigger(request):
    res, err = validateRequest(request.json, cancel_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)
# --------------------------------------------------------------


# SELL TRIGGER ENDPOINTS ---------------------------------------
@app.route(endpoints.sell_amount_endpoint, methods=['POST'])
async def setSellAmount(request):
    res, err = validateRequest(request.json, set_buy_amount_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)


@app.route(endpoints.sell_trigger_endpoint, methods=['POST'])
async def setSellTrigger(request):
    res, err = validateRequest(request.json, set_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)


@app.route(endpoints.cancel_sell_trigger_endpoint, methods=['POST'])
async def cancelSellTrigger(request):
    res, err = validateRequest(request.json, cancel_buy_trigger_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    return response.json(data)
# --------------------------------------------------------------


if __name__ == '__main__':
    app.register_listener(apiListeners.initAudit, 'before_server_start')
    app.register_listener(apiListeners.initTriggerExecutionManager, 'before_server_start')
    app.register_listener(apiListeners.initTriggerHandler, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')

    # Do after for initialising the active triggers in DB on start up
    app.register_listener(apiListeners.initActiveTriggers, 'before_server_start')

    app.register_listener(apiListeners.stopTriggerScheduler, 'before_server_stop')
    app.register_listener(apiListeners.closeHandlerClients, 'before_server_stop')

    app.run(
        host=config.TRIGGER_SERVER_IP,
        port=config.TRIGGER_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.RUN_DEBUG,
        auto_reload=True,
        workers=config.TRIGGER_SERVICE_WORKERS
    )
