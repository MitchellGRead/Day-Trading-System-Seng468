import TransactionConnections as Connections
from datetime import datetime
from math import floor, ceil
import pickle
from AuditHandler import AuditHandler


# TO DO:
# MONGO DB
# TRIGGERS
# Auditing - transaction numbers


# Get a current copy of DB for cache
def fillCache():
    # Fill account_balances cache
    dbmSocket.send(pickle.dumps({"command": "fillAccountCache"}))
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], pickle.dumps(user))

    # Fill stock_balances table
    dbmSocket.send(pickle.dumps({"command": "fillStockCache"}))
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), pickle.dumps(stockBalance))


# Updates Account Cache after a write
def updateAccountCache(userID):
    dbmSocket.send(pickle.dumps({"command": "updateAccountCache", "user_id": userID}))
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        user = {"user_id": row[0], "account_balance": row[1], "reserved_balance": row[2]}
        cache.set(row[0], pickle.dumps(user))


# Updates Stock Cache after a write
def updateStockCache(userID, stockSymbol):
    dbmSocket.send(pickle.dumps({"command": "updateStockCache", "user_id": userID, "stock_id": stockSymbol}))
    results = dbmSocket.recv(4096)
    results = pickle.loads(results)
    for row in results:
        stockBalance = {"user_id": row[0], "stock_id": row[1], "stock_amount": row[2], "stock_reserved": row[3]}
        cache.set("{}_{}".format(row[0], row[1]), pickle.dumps(stockBalance))


# Adds the amount to the users balance.
def add(userID, amount):
    dbmSocket.send(pickle.dumps({"command": "addFunds", "user_id": userID, "amount": amount}))
    result = dbmSocket.recv(1024).decode()
    print(result)
    updateAccountCache(userID)
    if result == "Success":
        return 1
    else:
        return f"Error Adding Funds In DBM for user {userID}"


# Gets a quote from the quote server and returns the information.
def quote(transaction_num, userID, stockSymbol):
    message = "{}, {}".format(stockSymbol, userID)
    stockSocket.send(message.encode())
    dataReceived = stockSocket.recv(1024).decode()
    dataReceived = dataReceived.split(", ")
    auditHandler.handleQuoteEvent(  # Ping to quote server
        transaction_num=transaction_num,
        user_name=userID,
        stock_symbol=stockSymbol,
        price=dataReceived[0],
        crptokey=dataReceived[2]
    )

    if cache.exists("quotes"):
        quotes = cache.get("quotes")
        quotes = pickle.loads(quotes)
        quotes[stockSymbol] = [dataReceived[0], datetime.now()]
        cache.set("quotes", pickle.dumps(quotes))
    else:
        quotes = {stockSymbol: [dataReceived[0], datetime.now()]}
        cache.set("quotes", pickle.dumps(quotes))
    print(dataReceived)
    return dataReceived[0]


# Creates a buy request to be confirmed by the user
def buy(transaction_num, userID, stockSymbol, amount):
    if cache.exists(userID):
        user = pickle.loads(cache.get(userID))
        price = float(quote(transaction_num, userID, stockSymbol))
        amountOfStock = floor(float(amount) / price)
        totalValue = price * amountOfStock

        if float(user["account_balance"]) >= float(amount):
            dictionary = {"user_id": userID, "stock_id": stockSymbol, "amount": totalValue,
                          "amount_of_stock": amountOfStock, "time": datetime.now()}
            cache.set(userID + "_BUY", pickle.dumps(dictionary))
            return 1
        else:
            return f"User {userID} does not have required funds."
    else:
        return f"User {userID} does not exist."


# Confirms the buy request
def commitBuy(userID):
    if cache.exists(userID + "_BUY"):
        buyObj = pickle.loads(cache.get(userID + "_BUY"))
        now = datetime.now()
        timeDiff = (now - buyObj["time"]).total_seconds()
        if timeDiff <= 60:
            dbmSocket.send(pickle.dumps({"command": "commitBuy", "user_id": userID, "value_amount": buyObj["amount"],
                                         "stock_id": buyObj["stock_id"], "amount_of_stock": buyObj["amount_of_stock"]}))
            result = dbmSocket.recv(1024).decode()
            cache.delete(userID + "_BUY")
            updateAccountCache(userID)
            updateStockCache(userID, buyObj["stock_id"])
            if result == "Success":
                return 1
            else:
                return "Error Committing Buy In DBM"
        else:
            cache.delete(userID + "_BUY")
            return "Buy too old."
    else:
        return f'No BUY exists for {userID}'


# Cancels the buy request
def cancelBuy(userID):
    if cache.exists(userID + "_BUY"):
        cache.delete(userID + "_BUY")
        return 1
    else:
        return "No buy to cancel."


# Creates a sell request to be confirmed by the user
def sell(transaction_num, userID, stockSymbol, amount):
    if cache.exists(userID + "_" + stockSymbol):
        user = pickle.loads(cache.get(userID + "_" + stockSymbol))
        price = float(quote(transaction_num, userID, stockSymbol))
        amountOfStock = ceil(float(amount) / price)
        totalValue = float(amount) * price

        if int(user["stock_amount"]) >= amountOfStock:
            dictionary = {"user_id": userID, "stock_id": stockSymbol,
                          "amount": totalValue, "amount_of_stock": amountOfStock, "time": datetime.now()}
            cache.set(userID + "_SELL", pickle.dumps(dictionary))
            return 1
        else:
            return 'User does not have required amount of that stock.'
    else:
        return f'User does not own stock {stockSymbol}.'


# Confirms the sell request
def commitSell(userID):
    if cache.exists(userID + "_SELL"):
        sellObj = pickle.loads(cache.get(userID + "_SELL"))
        now = datetime.now()
        timeDiff = (now - sellObj["time"]).total_seconds()
        if timeDiff <= 60:
            dbmSocket.send(pickle.dumps({"command": "commitSell", "user_id": userID, "value_amount": sellObj["amount"],
                                         "stock_id": sellObj["stock_id"],
                                         "amount_of_stock": sellObj["amount_of_stock"]}))
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
        return f"Sell does not exist for {userID}."


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
    global stockSocket, cache, dbmSocket, auditSocket, auditHandler

    dbmSocket = Connections.createDatabaseManagerConn()
    stockSocket = Connections.createQuoteConn()
    auditSocket = Connections.connectAudit()
    auditHandler = AuditHandler(auditSocket, Connections.serviceName)

    cache = Connections.startRedis()
    cache.flushdb()

    # Web connection
    webConn = Connections.connectWeb()
    while True:
        data = webConn.recv(1024)
        if not data:
            break
        data = pickle.loads(data)
        command = data["command"]

        if command == "ADD":
            response = add(data["user_id"], data["amount"])
            if response == 1:
                auditHandler.handleAddEvent(
                    transaction_num=data['transaction_num'],
                    user_name=data["user_id"],
                    funds=data["amount"]
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command='ADD',
                    error_msg=response,
                    user_name=data["user_id"],
                    funds=data["amount"]
                )
            print("received add command")

        elif command == "QUOTE":
            # Need work on WebService to accept quote info back.
            # Send response back to determine if service was hit or not?
            price = quote(data['transaction_num'], data["user_id"], data["stock_symbol"])
            response = 1
            print("received quote command")

        elif command == "BUY":
            response = buy(data['transaction_num'], data["user_id"], data["stock_symbol"], data["amount"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data["user_id"],
                    funds=data["amount"],
                    stock_symbol=data["stock_symbol"]
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data["user_id"],
                    funds=data["amount"],
                    stock_symbol=data["stock_symbol"]
                )
            print("received buy command")

        elif command == "COMMIT_BUY":
            response = commitBuy(data["user_id"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data['user_id']
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data['user_id']
                )
            print("received commit buy command")

        elif command == "CANCEL_BUY":
            response = cancelBuy(data["user_id"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data['user_id']
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data['user_id']
                )
            print("received cancel buy command")

        elif command == "SELL":
            response = sell(data['transaction_num'], data["user_id"], data["stock_symbol"], data["amount"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data['user_id'],
                    funds=data['amount'],
                    stock_symbol=data['stock_symbol']
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data['user_id'],
                    funds=data['amount'],
                    stock_symbol=data['stock_symbol']
                )
            print("received sell command")

        elif command == "COMMIT_SELL":
            response = commitSell(data["user_id"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data['user_id']
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data['user_id']
                )
            print("received commit sell command")

        elif command == "CANCEL_SELL":
            response = cancelSell(data["user_id"])
            if response == 1:
                auditHandler.handleUserCommandEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    user_name=data['user_id']
                )
            else:
                auditHandler.handleErrorEvent(
                    transaction_num=data['transaction_num'],
                    command=command,
                    error_msg=response,
                    user_name=data['user_id']
                )
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
        webConn.send(pickle.dumps(response))
