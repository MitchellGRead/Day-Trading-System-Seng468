import TransactionConnections as Connections
import datetime
import json
from math import floor, ceil
import pickle

# TO DO:
# MONGO DB
# TRIGGERS
# Auditing


# Time Handling Method
def default(obj):
    if isinstance(obj, datetime.datetime):
        return {'_isoformat': obj.isoformat()}
    return super().default(obj)


# Time Handling Method
def object_hook(obj):
    _isoformat = obj.get('_isoformat')
    if _isoformat is not None:
        return datetime.datetime.fromisoformat(_isoformat)
    return obj


# Get a current copy of DB for cache
def fillCache():
    # Fill account_balances cache
    dbmSocket.send(json.dumps({"command": "fillAccountCache"}).encode())
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], json.dumps(user))

    # Fill stock_balances table
    dbmSocket.send(json.dumps({"command": "fillStockCache"}).encode())
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), json.dumps(stockBalance))


# Updates Account Cache after a write
def updateAccountCache(userID):
    dbmSocket.send(json.dumps({"command": "updateAccountCache", "user_id": userID}).encode())
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], json.dumps(user))


# Updates Stock Cache after a write
def updateStockCache(userID, stockSymbol):
    dbmSocket.send(json.dumps({"command": "updateStockCache", "user_id": userID, "stock_id": stockSymbol}).encode())
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), json.dumps(stockBalance))


# Adds the amount to the users balance.
def add(userID, amount):
    dbmSocket.send(json.dumps({"command": "addFunds", "user_id": userID, "amount": amount}).encode())
    result = dbmSocket.recv(1024).decode()
    updateAccountCache(userID)
    if result == "Success":
        return 1
    else:
        return "Error Adding Funds In DBM"


# Gets a quote from the quote server and returns the information.
def quote(userID, stockSymbol):
    message = "{}, {}".format(stockSymbol, userID)
    stockSocket.send(message.encode())
    dataReceived = stockSocket.recv(1024).decode()
    dataReceived = dataReceived.split(", ")

    if cache.exists("quotes"):
        quotes = cache.get("quotes")
        quotes = json.loads(quotes, object_hook=object_hook)
        quotes[stockSymbol] = [dataReceived[0], datetime.datetime.now()]
        cache.set("quotes", json.dumps(quotes, default=default))
    else:
        quotes = {stockSymbol: [dataReceived[0], datetime.datetime.now()]}
        cache.set("quotes", json.dumps(quotes, default=default))
    print(dataReceived)
    return dataReceived[0]


# Creates a buy request to be confirmed by the user
def buy(userID, stockSymbol, amount):
    if cache.exists(userID):
        user = json.loads(cache.get(userID))
        price = float(quote(userID, stockSymbol))
        amountOfStock = floor(float(amount) / price)
        totalValue = price * amountOfStock

        if float(user["account_balance"]) >= float(amount):
            dictionary = {"user_id": userID, "stock_id": stockSymbol, "amount": totalValue,
                          "amount_of_stock": amountOfStock, "time": datetime.datetime.now()}
            cache.set(userID + "_BUY", json.dumps(dictionary, default=default))
            return 1
        else:
            return "User does not have required funds."
    else:
        return "User does not exist."


# Confirms the buy request
def commitBuy(userID):
    if cache.exists(userID + "_BUY"):
        buyObj = json.loads(cache.get(userID + "_BUY"), object_hook=object_hook)
        now = datetime.datetime.now()
        timeDiff = (now - buyObj["time"]).total_seconds()
        if timeDiff <= 60:
            dbmSocket.send(json.dumps({"command": "commitBuy", "user_id": userID, "value_amount": buyObj["amount"],
                                       "stock_id": buyObj["stock_id"], "amount_of_stock": buyObj["amount_of_stock"]}
                                      ).encode())
            result = dbmSocket.recv(1024).decode()
            cache.delete(userID + "_BUY")
            updateAccountCache(userID)
            updateStockCache(userID, json.dumps(buyObj["stock_id"]))
            if result == "Success":
                return 1
            else:
                return "Error Committing Buy In DBM"
        else:
            cache.delete(userID + "_BUY")
            return "Buy too old."
    else:
        return "No buy exists."


# Cancels the buy request
def cancelBuy(userID):
    if cache.exists(userID + "_BUY"):
        cache.delete(userID + "_BUY")
        return 1
    else:
        return "No buy to cancel."


# Creates a sell request to be confirmed by the user
def sell(userID, stockSymbol, amount):
    if cache.exists(userID + "_" + stockSymbol):
        user = json.loads(cache.get(userID + "_" + stockSymbol))
        price = float(quote(userID, stockSymbol))
        amountOfStock = ceil(float(amount) / price)
        totalValue = float(amount) * price

        if int(user["stock_amount"]) >= amountOfStock:
            dictionary = {"user_id": userID, "stock_id": stockSymbol,
                          "amount": totalValue, "amount_of_stock": amountOfStock, "time": datetime.datetime.now()}
            cache.set(userID + "_SELL", json.dumps(dictionary, default=default))
            return 1
        else:
            return "User does not have required amount of that stock."
    else:
        return "User does not have that stock."


# Confirms the sell request
def commitSell(userID):
    if cache.exists(userID + "_SELL"):
        sellObj = json.loads(cache.get(userID + "_SELL"), object_hook=object_hook)
        now = datetime.datetime.now()
        timeDiff = (now - sellObj["time"]).total_seconds()
        if timeDiff <= 60:
            dbmSocket.send(json.dumps({"command": "commitSell", "user_id": userID, "value_amount": sellObj["amount"],
                                       "stock_id": sellObj["stock_id"], "amount_of_stock": sellObj["amount_of_stock"]}
                                      ).encode())
            result = dbmSocket.recv(1024).decode()

            cache.delete(userID + "_SELL")
            updateAccountCache(userID)
            updateStockCache(userID, sellObj["stock_id"])
            if result == "Success":
                return 1
            else:
                return "Error Committing Buy In DBM"
        else:
            cache.delete(userID + "_SELL")
            return "Sell too old."
    else:
        return "Sell does not exist."


# Cancels the sell request
def cancelSell(userID):
    if cache.exists(userID + "_SELL"):
        cache.delete(userID + "_SELL")
        return 1
    else:
        return "No sell to cancel"


def setBuyAmount(userID, stockSymbol, amount):
    print("to do")


def cancelSetBuy(userID, stockSymbol):
    print("to do")


def setBuyTrigger(userID, stockSymbol, amount):
    print("to do")


def setSellAmount(userID, stockSymbol, amount):
    print("to do")


def cancelSetSell(userID, stockSymbol):
    print("to do")


def setSellTrigger(userID, stockSymbol, amount):
    print("to do")


if __name__ == "__main__":
    print("Start program")
    global stockSocket, cache, dbmSocket

    dbmSocket = Connections.createDatabaseManagerConn()
    stockSocket = Connections.createQuoteConn()

    cache = Connections.startRedis()
    cache.flushdb()


    # Web connection
    webConn = Connections.connectWeb()
    while True:
        data = webConn.recv(1024)
        if not data:
            break
        msg = data.decode()
        data = json.loads(msg)
        command = data["command"]
        if command == "DISPLAY_SUMMARY":
            response = 1
            print("received display summary command")
        elif command == "DUMPLOG":
            response = 1
            print("received dumplog command")

        elif command == "ADD":
            response = add(data["user_id"], data["amount"])
            print("received add command")
        elif command == "QUOTE":
            # Need work on WebService to accept quote info back.
            price = quote(data["user_id"], data["stock_symbol"])
            response = 1
            print("received quote command")

        elif command == "BUY":
            response = buy(data["user_id"], data["stock_symbol"], data["amount"])
            print("received buy command")
        elif command == "COMMIT_BUY":
            response = commitBuy(data["user_id"])
            print("received commit buy command")
        elif command == "CANCEL_BUY":
            response = cancelBuy(data["user_id"])
            print("received cancel buy command")

        elif command == "SELL":
            response = sell(data["user_id"], data["stock_symbol"], data["amount"])
            print("received sell command")
        elif command == "COMMIT_SELL":
            response = commitSell(data["user_id"])
            print("received commit sell command")
        elif command == "CANCEL_SELL":
            response = cancelSell(data["user_id"])
            print("received cancel sell command")

        # Not Implemented
        elif command == "SET_BUY_AMOUNT":
            response = 1
            print("received set buy amount command")
        elif command == "SET_BUY_TRIGGER":
            response = 1
            print("received set buy trigger command")
        elif command == "CANCEL_SET_BUY":
            response = 1
            print("received cancel set buy command")

        # Not Implemented
        elif command == "SET_SELL_AMOUNT":
            response = 1
            print("received set sell amount command")
        elif command == "SET_SELL_TRIGGER":
            response = 1
            print("received set sell trigger command")
        elif command == "CANCEL_SET_SELL":
            response = 1
            print("received cancel set sell command")

        else:
            response = "Unknown command"
            print(data)
            print("received unknown command")

        # Format response
        if response == 1:
            response = {"status": 200}
        else:
            response = {"status": 500, "reason": response}
        webConn.send(json.dumps(response).encode())
