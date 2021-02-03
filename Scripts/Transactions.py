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


# Adds the amount to the users balance.
# TO DO: AUDIT
def add(userID, amount):
    if cache.exists(userID):
        query = "UPDATE {TABLE} SET account_balance = account_balance + {AMOUNT} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID, AMOUNT=amount)
        Connections.executeQuery(dbConnection, query)

        cachedUser = cache.get(userID)
        query = "SELECT account_balance FROM {TABLE} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID)
        currentBal = Connections.executeReadQuery(dbConnection, query)
        cachedUser['account_balance'] = currentBal[0]
    else:
        query = "INSERT INTO {TABLE} (user_id, account_balance, reserve_balance) VALUES ({USER}, {BALANCE}, 0)".format(
                TABLE=accountBalancesTable, USER=userID, BALANCE=amount)
        Connections.executeQuery(dbConnection, query)

        query = "INSERT INTO {TABLE} (user_id) VALUE {USER}".format(TABLE=usersTable, USER=userID)
        Connections.executeQuery(dbConnection, query)

        query = "SELECT * FROM {TABLE} WHERE user_id = {USER}".format(
                TABLE=accountBalancesTable, USER=userID)
        userInfo = Connections.executeReadQuery(dbConnection, query)
        user = {"user_id": userInfo[0], "account_balance": userInfo[1], "reserve_balance": userInfo[2]}
        cache.set(userID, user)


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
    return dataReceived


def buy(userID, stockSymbol, amount):
    print("to do")


def commitBuy(userID):
    print("to do")


def cancelBuy(userID):
    print("to do")


def sell(userID, stockSymbol, amount):
    print("to do")


def commitSell(userID):
    print("to do")


def cancelSell(userID):
    print("to do")


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
