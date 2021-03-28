
from sanic import Sanic, response

import apiListeners
import config
import endpoints
from auditInputSchema import *

app = Sanic(config.AUDIT_SERVER_NAME)


@app.route(endpoints.account_summary, methods=['GET'])
async def accountSummary(request, command, trans_num, user_id):
    data = {
        'transaction_num': trans_num,
        'command': command,
        'user_id': user_id
    }
    res, err = validateRequest(data, account_summary_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    resp, status = await app.config['logic'].fetchAccountSummary(data)
    return response.json(resp, status=status)

@app.route(endpoints.generate_dumplog, methods=['GET'])
async def generateDumplog(request, command, trans_num, filename):
    user_id = request.args.get('user_id', '')
    data = {
        'command': command,
        'transaction_num': trans_num,
        'filename': filename
    }
    if user_id:
        data['user_id'] = user_id

    res, err = validateRequest(data, dumplog_schema)
    if not res:
        return response.json(errorResult(err, data), status=400)

    resp, status = await app.config['logic'].generateDumplog(data)
    return response.json(data)

@app.route(endpoints.user_command_endpoint, methods=['POST'])
async def userCommandEvent(request):
    res, err = validateRequest(request.json, user_command_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    data['xmlName'] = 'userCommand'
    await app.config['logic'].logEvent(data)
    return response.json(request.json)


@app.route(endpoints.account_transaction_endpoint, methods=['POST'])
async def accountTransactionEvent(request):
    res, err = validateRequest(request.json, account_transaction_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    data['xmlName'] = 'accountTransaction'
    await app.config['logic'].logEvent(data)
    return response.json(request.json)


@app.route(endpoints.system_endpoint, methods=['POST'])
async def systemEvent(request):
    res, err = validateRequest(request.json, system_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    data['xmlName'] = 'systemEvent'
    await app.config['logic'].logEvent(data)
    return response.json(request.json)


@app.route(endpoints.quote_server_endpoint, methods=['POST'])
async def quoteServerEvent(request):
    res, err = validateRequest(request.json, quote_server_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    data['xmlName'] = 'quoteServer'
    await app.config['logic'].logEvent(data)
    return response.json(request.json)


@app.route(endpoints.error_endpoint, methods=['POST'])
async def errorEvent(request):
    res, err = validateRequest(request.json, error_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    data = request.json
    data['xmlName'] = 'errorEvent'
    await app.config['logic'].logEvent(data)
    return response.json(request.json)


if __name__ == '__main__':
    app.register_listener(apiListeners.initDbmHanlder, 'before_server_start')
    app.register_listener(apiListeners.initServiceLogic, 'before_server_start')


    app.run(
        host=config.AUDIT_SERVER_IP,
        port=config.AUDIT_SERVER_PORT,
        debug=config.RUN_DEBUG,
        access_log=config.ACCESS_LOGS,
        auto_reload=True,
        workers=config.AUDIT_SERVER_WORKERS
    )
