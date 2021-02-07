import Connections
import datetime
import json

usersTable = "users"
accountBalancesTable = "accounts"
stockBalancesTable = "stocks"


# TO DO:
# MONGO DB
# TRIGGERS
# Auditing


# Get a current copy of DB for cache
def fillCache():
    # Fill account_balances cache
    query = "SELECT * FROM {TABLE}".format(TABLE=accountBalancesTable)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], json.dumps(user))

    # Fill stock_balances table
    query = "SELECT * FROM {TABLE}".format(TABLE=stockBalancesTable)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), json.dumps(stockBalance))


# Updates Account Cache after a write
def updateAccountCache(userID):
    query = "SELECT * FROM {TABLE} WHERE user_id = {USER}".format(TABLE=accountBalancesTable, USER=userID)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], json.dumps(user))


# Updates Stock Cache after a write
def updateStockCache(userID, stockSymbol):
    query = "SELECT * FROM {TABLE} WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                                         USER=userID,
                                                                                         STOCK=stockSymbol)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), json.dumps(stockBalance))


# Adds the amount to the users balance.
def add(userID, amount):
    if cache.exists(userID):
        query = "UPDATE {TABLE} SET account_balance = account_balance + {AMOUNT} WHERE user_id = {USER}".format(
            TABLE=accountBalancesTable, USER=userID, AMOUNT=amount)
        Connections.executeQuery(dbConnection, query)

        updateAccountCache(userID)
    else:
        query = "INSERT INTO {TABLE} (user_id, account_balance, reserve_balance) VALUES ({USER}, {BALANCE}, 0)".format(
            TABLE=accountBalancesTable, USER=userID, BALANCE=amount)
        Connections.executeQuery(dbConnection, query)

        query = "INSERT INTO {TABLE} (user_id) VALUE {USER}".format(TABLE=usersTable, USER=userID)
        Connections.executeQuery(dbConnection, query)

        updateAccountCache(userID)
    return 1


# Gets a quote from the quote server and returns the information.
def quote(userID, stockSymbol):
    message = "{}, {}".format(stockSymbol, userID)
    stockSocket.send(message.encode())
    dataReceived = stockSocket.recv(1024).decode()
    dataReceived = dataReceived.split(", ")

    if cache.exists("quotes"):
        quotes = cache.get("quotes")
        quotes[stockSymbol] = [dataReceived[0], datetime.datetime.now()]
        cache.set("quotes", quotes)
    else:
        quotes = {stockSymbol: [dataReceived[0], datetime.datetime.now()]}
        cache.set("quotes", quotes)
    return dataReceived[0]


# Creates a buy request to be confirmed by the user
def buy(userID, stockSymbol, amount):
    if cache.exists(userID):
        user = cache.get(userID)
        price = quote(userID, stockSymbol)
        value = amount * price
        if user["account_balance"] >= value:
            cache.set(userID + "_BUY", {"user_id": userID, "stock_id": stockSymbol,
                                        "amount": amount, "value": value, "time": datetime.datetime.now()})
            return 1
        else:
            return "User does not have required funds."
    else:
        return "User does not exist."


# Confirms the buy request
def commitBuy(userID):
    if cache.exists(userID + "_BUY"):
        buyObj = cache.get(userID + "_BUY")
        now = datetime.datetime.now()
        timeDiff = (now - buyObj["time"]).total_seconds()
        if timeDiff <= 60:
            query = "UPDATE {TABLE} SET account_balance = account_balance - {AMOUNT} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID, AMOUNT=buyObj["value"])
            Connections.executeQuery(dbConnection, query)
            query = "SELECT EXISTS(SELECT * FROM {TABLE} WHERE user_id = {USER} AND stock_id = {STOCK})".format(
                TABLE=stockBalancesTable, USER=userID, STOCK=buyObj["stock_id"])
            if Connections.executeExist(dbConnection, query):
                query = "UPDATE {TABLE} SET stock_amount = stock_amount + {AMOUNT} " \
                        "WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                               AMOUNT=buyObj['amount'],
                                                                               USER=userID,
                                                                               STOCK=buyObj["stock_id"])
                Connections.executeQuery(dbConnection, query)
            else:
                query = "INSERT INTO {TABLE} VALUES" \
                        " ({USER}, {STOCK}, {AMOUNT}, 0)".format(TABLE=stockBalancesTable, AMOUNT=buyObj['amount'],
                                                                 USER=userID, STOCK=buyObj["stock_id"])
                Connections.executeQuery(dbConnection, query)

            cache.delete(userID + "_BUY")
            updateAccountCache(userID)
            updateStockCache(userID, buyObj["stock_id"])
            return 1
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
        user = cache.get(userID)
        price = quote(userID, stockSymbol)
        value = amount * price
        if user["stock_amount"] >= amount:
            cache.set(userID + "_SELL", {"user_id": userID, "stock_id": stockSymbol,
                                         "amount": amount, "value": value, "time": datetime.datetime.now()})
            return 1
        else:
            return "User does not have required amount of that stock."
    else:
        return "User does not have that stock."


# Confirms the sell request
def commitSell(userID):
    if cache.exists(userID + "_SELL"):
        sellObj = cache.get(userID + "_SELL")
        now = datetime.datetime.now()
        timeDiff = (now - sellObj["time"]).total_seconds()
        if timeDiff <= 60:
            query = "UPDATE {TABLE} SET account_balance = account_balance + {AMOUNT} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID, AMOUNT=sellObj["value"])
            Connections.executeQuery(dbConnection, query)
            query = "UPDATE {TABLE} SET stock_amount = stock_amount - {AMOUNT} " \
                    "WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                           AMOUNT=sellObj['amount'],
                                                                           USER=userID,
                                                                           STOCK=sellObj["stock_id"])
            Connections.executeQuery(dbConnection, query)

            cache.delete(userID + "_SELL")
            updateAccountCache(userID)
            updateStockCache(userID, sellObj["stock_id"])
            return 1
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
    global stockSocket, dbConnection, cache

    dbConnection = Connections.createSQLConnection()
    Connections.checkDB(dbConnection)

    # Figuring out redis, will need to rejigger above methods
    # Need to run redis-server.exe
    cache = Connections.startRedis()
    testCache = {"test": "cache", "cache": "test"}
    cache.set("test", json.dumps(testCache))

    print(json.loads(cache.get("test")))

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
            response = 1
            print("received add command")
        elif command == "QUOTE":
            response = 1
            print("received quote command")
        elif command == "BUY":
            response = 1
            print("received buy command")
        elif command == "COMMIT_BUY":
            response = 1
            print("received commit buy command")
        elif command == "CANCEL_BUY":
            response = 1
            print("received cancel buy command")
        elif command == "SET_BUY_AMOUNT":
            response = 1
            print("received set buy amount command")
        elif command == "SET_BUY_TRIGGER":
            response = 1
            print("received set buy trigger command")
        elif command == "CANCEL_SET_BUY":
            response = 1
            print("received cancel set buy command")
        elif command == "SELL":
            response = 1
            print("received sell command")
        elif command == "COMMIT_SELL":
            response = 1
            print("received commit sell command")
        elif command == "CANCEL_SELL":
            response = 1
            print("received cancel sell command")
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

    stockSocket = Connections.createQuoteConn()

    fillCache()

    quote('oY01WVirLr', 'S')
