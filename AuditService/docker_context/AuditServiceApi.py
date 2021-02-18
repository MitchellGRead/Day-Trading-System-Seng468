
from sanic import Sanic, response
import aiohttp

import config
from auditInputSchema import *
import endpoints

app = Sanic(config.AUDIT_SERVER_NAME)


@app.route(endpoints.user_command_endpoint, methods=['POST'])
async def userCommandEvent(request):
    res, err = validateRequest(request.json, user_command_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    print(request.json)
    return response.json(request.json)


@app.route(endpoints.system_endpoint, methods=['POST'])
async def systemEvent(request):
    res, err = validateRequest(request.json, system_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    print(request.json)
    return response.json(request.json)


@app.route(endpoints.quote_server_endpoint, methods=['POST'])
async def quoteServerEvent(request):
    res, err = validateRequest(request.json, quote_server_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    print(request.json)
    return response.json(request.json)


@app.route(endpoints.error_endpoint, methods=['POST'])
async def errorEvent(request):
    res, err = validateRequest(request.json, error_event_schema)
    if not res:
        return response.json(errorResult(err, request.json), status=400)

    print(request.json)
    return response.json(request.json)


if __name__ == '__main__':
    app.run(
        host=config.AUDIT_SERVER_IP,
        port=config.AUDIT_SERVER_PORT,
        debug=config.RUN_DEBUG,
        auto_reload=True
    )