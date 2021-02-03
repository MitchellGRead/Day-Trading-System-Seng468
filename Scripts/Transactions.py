import Connections
import datetime

usersTable = "TBD"
accountBalancesTable = "TBD"
stockBalancesTable = "TBD"


# Get a current copy of DB for cache
def fillCache():
    # Fill account_balances cache
    query = "SELECT * FROM {TABLE}".format(TABLE=accountBalancesTable)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], user)

    # Fill stock_balances table
    query = "SELECT * FROM {TABLE}".format(TABLE=stockBalancesTable)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), stockBalance)


# Updates Account Cache after a write
def updateAccountCache(userID):
    query = "SELECT * FROM {TABLE} WHERE user_id = {USER}".format(TABLE=accountBalancesTable, USER=userID)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], user)


# Updates Stock Cache after a write
def updateStockCache(userID, stockSymbol):
    query = "SELECT * FROM {TABLE} WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                                         USER=userID,
                                                                                         STOCK=stockSymbol)
    results = Connections.executeReadQuery(connection=dbConnection, query=query)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), stockBalance)


# Adds the amount to the users balance.
# TO DO: AUDIT
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


# Gets a quote from the quote server and returns the information.
# TO DO: AUDIT
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


# TO DO: MONGODB PORTION
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
            return "Error: User does not have required funds."
    else:
        return "Error: User does not exist."


def commitBuy(userID):
    if cache.exists(userID + "_BUY"):
        buy = cache.get(userID + "_BUY")
        now = datetime.datetime.now()
        timeDiff = (now - buy["time"]).total_seconds()
        if timeDiff <= 60:
            query = "UPDATE {TABLE} SET account_balance = account_balance - {AMOUNT} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID, AMOUNT=buy["value"])
            Connections.executeQuery(dbConnection, query)
            query = "SELECT EXISTS(SELECT * FROM {TABLE} WHERE user_id = {USER} AND stock_id = {STOCK})".format(
                TABLE=stockBalancesTable, USER=userID, STOCK=buy["stock_id"])
            if Connections.executeExist(dbConnection, query):
                query = "UPDATE {TABLE} SET stock_amount = stock_amount + {AMOUNT} " \
                        "WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                               AMOUNT=buy['amount'],
                                                                               USER=userID,
                                                                               STOCK=buy["stock_id"])
                Connections.executeQuery(dbConnection, query)
            else:
                query = "INSERT INTO {TABLE} VALUES" \
                        " ({USER}, {STOCK}, {AMOUNT}, 0)".format(TABLE=stockBalancesTable, AMOUNT=buy['amount'],
                                                                 USER=userID, STOCK=buy["stock_id"])
                Connections.executeQuery(dbConnection, query)

            cache.delete(userID + "_BUY")
            updateAccountCache(userID)
            updateStockCache(userID, buy["stock_id"])
            return 1
        else:
            cache.delete(userID + "_BUY")
            return "Error: Buy too old"


# TO DO MongoDB Portion
def cancelBuy(userID):
    if cache.exists(userID + "_BUY"):
        cache.delete(userID + "_BUY")
        return 1
    else:
        return "Error: No buy to cancel"


def sell(userID, stockSymbol, amount):
    if cache.exists(userID+"_"+stockSymbol):
        user = cache.get(userID)
        price = quote(userID, stockSymbol)
        value = amount * price
        if user["stock_amount"] >= amount:
            cache.set(userID + "_SELL", {"user_id": userID, "stock_id": stockSymbol,
                                        "amount": amount, "value": value, "time": datetime.datetime.now()})
            return 1
        else:
            return "Error: User does not have required amount of that stock."
    else:
        return "Error: User does not have that stock."


def commitSell(userID):
    if cache.exists(userID + "_SELL"):
        sell = cache.get(userID + "_SELL")
        now = datetime.datetime.now()
        timeDiff = (now - sell["time"]).total_seconds()
        if timeDiff <= 60:
            query = "UPDATE {TABLE} SET account_balance = account_balance + {AMOUNT} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID, AMOUNT=sell["value"])
            Connections.executeQuery(dbConnection, query)
            query = "UPDATE {TABLE} SET stock_amount = stock_amount - {AMOUNT} " \
                    "WHERE user_id = {USER} AND stock_id = {STOCK}".format(TABLE=stockBalancesTable,
                                                                           AMOUNT=buy['amount'],
                                                                           USER=userID,
                                                                           STOCK=buy["stock_id"])
            Connections.executeQuery(dbConnection, query)

            cache.delete(userID + "_SELL")
            updateAccountCache(userID)
            updateStockCache(userID, sell["stock_id"])
            return 1
        else:
            cache.delete(userID + "_SELL")
            return "Error: Sell too old"


def cancelSell(userID):
    if cache.exists(userID + "_SELL"):
        cache.delete(userID + "_SELL")
        return 1
    else:
        return "Error: No sell to cancel"


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

    stockSocket = Connections.createQuoteConn()
    dbConnection = Connections.createDBConnection()
    cache = Connections.startRedis()

    fillCache()

    quote('oY01WVirLr', 'S')
