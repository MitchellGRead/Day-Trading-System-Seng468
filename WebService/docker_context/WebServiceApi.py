from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

WEBSERVER_IP = "localhost"
WEBSERVER_PORT = 5000
SUCCESS_CODE = 200



@app.route('/', methods=['GET'])
def home():
    return 'Hello world!'


@app.route('/add/funds/', methods=['POST'])
def addToAccount():
    if checkRequest(request):
        raise Exception("No json or user_id in /add/funds/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/quote/<string:user_id>/<string:stock_symbol>/', methods=['GET'])
def getSymbolQuote(user_id, stock_symbol):
    print(user_id, stock_symbol)
    return jsonify({'user_id': user_id, 'stock_symbol': stock_symbol})


@app.route('/summary/<string:user_id>/', methods=['GET'])
def displayUserSummary(user_id):
    print(user_id)
    return jsonify({'user_id': user_id})


@app.route('/dumplog/', methods=['GET'])
def dumplog():
    return jsonify({'command': 'all user dumplog'})


@app.route('/dumplog/<string:user_id>/', methods=['GET'])
def userDumplog(user_id):
    return jsonify({'command': 'dumplog', 'user_id': user_id})


# BUY ROUTES ----------------------------------------------
@app.route('/buy/', methods=['POST'])
def buySymbol():
    if checkRequest(request):
        raise Exception("No json or user_id in /buy/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/buy/commit/', methods=['POST'])
def commitBuy():
    if checkRequest(request):
        raise Exception("No json or user_id in /buy/commit/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/cancel/buy/', methods=['POST'])
def cancelBuy():
    if checkRequest(request):
        raise Exception("No json or user_id in /cancel/buy/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/set/buy/amount/', methods=['POST'])
def setBuyAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /buy/amount/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/cancel/set/buy/', methods=['POST'])
def cancelSetBuyAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /cancel/set/buy/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/set/buy/trigger/', methods=['POST'])
def setBuyTriggerAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /set/buy/trigger/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE
# ----------------------------------------------------------


# SELL ROUTES ----------------------------------------------
@app.route('/sell/', methods=['POST'])
def sellSymbol():
    if checkRequest(request):
        raise Exception("No json or user_id in /sell/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/sell/commit/', methods=['POST'])
def commitSell():
    if checkRequest(request):
        raise Exception("No json or user_id in /sell/commit/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/cancel/sell/', methods=['POST'])
def cancelSell():
    if checkRequest(request):
        raise Exception("No json or user_id in /cancel/sell/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/set/sell/amount/', methods=['POST'])
def setSellAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /sell/amount/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/cancel/set/sell/', methods=['POST'])
def cancelSetSellAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /cancel/set/sell/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE


@app.route('/set/sell/trigger/', methods=['POST'])
def setSellTriggerAmount():
    if checkRequest(request):
        raise Exception("No json or user_id in /set/sell/trigger/ call")

    # TODO("make call to trans server")
    print(request.json)
    return jsonify(request.json), SUCCESS_CODE
# ----------------------------------------------------------


def checkRequest(api_request):
    return not api_request.json or 'user_id' not in api_request.json


if __name__ == '__main__':
    app.run(host=WEBSERVER_IP, port=WEBSERVER_PORT)
