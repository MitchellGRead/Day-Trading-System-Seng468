import pickle
import DatabaseManagerConnections as Connections

usersTable = "users"
accountBalancesTable = "accounts"
stockBalancesTable = "stocks"
triggersTable = "triggers"


def fillAccountCache():
    query = "SELECT * FROM {TABLE};".format(TABLE=accountBalancesTable)
    print(query)
    results = Connections.executeReadQuery(connection=sqlConnection, query=query)
    return results


def fillStockCache():
    query = "SELECT * FROM {TABLE};".format(TABLE=stockBalancesTable)
    print(query)
    results = Connections.executeReadQuery(connection=sqlConnection, query=query)
    return results


def updateAccountCache(userID):
    query = "SELECT * FROM {TABLE} WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID)
    print(query)
    results = Connections.executeReadQuery(connection=sqlConnection, query=query)
    return results


def updateStockCache(userID, stockSymbol):
    query = "SELECT * FROM {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}';".format(
        TABLE=stockBalancesTable, USER=userID, STOCK=stockSymbol)
    print(query)
    results = Connections.executeReadQuery(connection=sqlConnection, query=query)
    return results


def addUser(userID):
    query = "SELECT exists (SELECT 1 FROM {TABLE} " \
            "WHERE user_id = '{USER}' LIMIT 1);".format(TABLE=usersTable, USER=userID)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        return
    else:
        print("Adding user " + userID)
        query = "INSERT INTO {TABLE} (user_id) VALUES ('{USER}');".format(TABLE=usersTable, USER=userID)
        print(query)
        Connections.executeQuery(sqlConnection, query)


def addFunds(userID, amount):
    query = "SELECT exists (SELECT 1 FROM {TABLE} " \
            "WHERE user_id = '{USER}' LIMIT 1);".format(TABLE=accountBalancesTable, USER=userID)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        query = "UPDATE {TABLE} SET account_balance = account_balance" \
                " + {AMOUNT} WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID, AMOUNT=amount)
        print(query)
        Connections.executeQuery(sqlConnection, query)
    else:
        addUser(userID)
        query = "INSERT INTO {TABLE} (user_id, account_balance, reserve_balance) VALUES ('{USER}', {BALANCE}, " \
                "0);".format(TABLE=accountBalancesTable, USER=userID, BALANCE=amount)
        print(query)
        Connections.executeQuery(sqlConnection, query)
    return 1


def commitBuy(userID, stockSymbol, valueAmount, stockAmount):
    query = "UPDATE {TABLE} SET account_balance = account_balance - {AMOUNT} " \
            "WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID, AMOUNT=valueAmount)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    query = "SELECT EXISTS(SELECT * FROM {TABLE} WHERE user_id = '{USER}' AND " \
            "stock_id = '{STOCK}');".format(TABLE=stockBalancesTable, USER=userID, STOCK=stockSymbol)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        query = "UPDATE {TABLE} SET stock_amount = stock_amount + {AMOUNT} WHERE user_id = '{USER}' AND stock_id = " \
                "'{STOCK}';".format(TABLE=stockBalancesTable, AMOUNT=stockAmount, USER=userID, STOCK=stockSymbol)
        print(query)
        Connections.executeQuery(sqlConnection, query)
    else:
        addUser(userID)
        query = "INSERT INTO {TABLE} VALUES ('{USER}', '{STOCK}', {AMOUNT}, " \
                "0);".format(TABLE=stockBalancesTable, AMOUNT=stockAmount, USER=userID, STOCK=stockSymbol)
        print(query)
        Connections.executeQuery(sqlConnection, query)
    return 1


def commitSell(userID, stockSymbol, valueAmount, stockAmount):
    query = "UPDATE {TABLE} SET account_balance = account_balance + {AMOUNT} WHERE " \
            "user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID, AMOUNT=valueAmount)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    query = "UPDATE {TABLE} SET stock_amount = stock_amount - {AMOUNT} WHERE user_id = '{USER}' AND stock_id = " \
            "'{STOCK}';".format(TABLE=stockBalancesTable, AMOUNT=stockAmount, USER=userID, STOCK=stockSymbol)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    return 1


def setBuyAmount(userID, stockSymbol, stockAmount):
    query = "SELECT EXISTS(SELECT 1 from {TABLE} where user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'buy' LIMIT 1);".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        return {'error': "A buy option for this stock already exists."}
    else:
        query = "INSERT INTO {TABLE} (user_id, stock_id, type, amount) VALUES " \
                "('{USER}', '{STOCK}', 'buy', {AMOUNT});".format(TABLE=triggersTable, USER=userID,
                                                                 STOCK=stockSymbol, AMOUNT=stockAmount)
        print(query)
        Connections.executeQuery(sqlConnection, query)
        return 1


def setBuyTrigger(userID, stockSymbol, price):
    price = float(price)
    query = "SELECT EXISTS(SELECT 1 from {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'buy' LIMIT 1);".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        query = "SELECT account_balance FROM {TABLE} WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable,
                                                                                       USER=userID)
        print(query)
        result = Connections.executeReadQuery(sqlConnection, query)
        balance = result[0][0]
        query = "SELECT amount FROM {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
                "AND type = 'buy'".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
        print(query)
        result = Connections.executeReadQuery(sqlConnection, query)
        stockAmount = result[0][0]
        reserveNeeded = stockAmount * price
        if reserveNeeded > balance:
            return {'error': "The user doesn't have the needed amount of funds"}
        else:
            newBalance = balance - reserveNeeded
            query = "UPDATE {TABLE} SET account_balance = {BALANCE}, reserve_balance = {RESERVE} " \
                    "WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID,
                                                       BALANCE=newBalance, RESERVE=reserveNeeded)
            print(query)
            Connections.executeQuery(sqlConnection, query)
            query = "UPDATE {TABLE} SET trigger = {PRICE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
                    "AND type = 'buy'".format(TABLE=triggersTable, PRICE=price, USER=userID, STOCK=stockSymbol)
            print(query)
            Connections.executeQuery(sqlConnection, query)
            return 1
    else:
        return {'error': "No set buy exists."}


def cancelBuyTrigger(userID, stockSymbol):
    query = "DELETE FROM {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'buy'".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    query = "UPDATE {TABLE} SET account_balance = account_balance + reserve_balance, reserve_balance = 0 " \
            "WHERE user_id = '{USER}';".format(TABLE=accountBalancesTable, USER=userID)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    return 1


def setSellAmount(userID, stockSymbol, stockAmount):
    stockAmount = float(stockAmount)
    query = "SELECT EXISTS(SELECT 1 from {TABLE} where user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'sell' LIMIT 1);".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        return {'error': "A sell option for this stock already exists."}
    else:
        query = "SELECT EXISTS(SELECT 1 from {TABLE} where user_id = '{USER}' AND stock_id = '{STOCK}' " \
                "LIMIT 1);".format(TABLE=stockBalancesTable, USER=userID, STOCK=stockSymbol)
        print(query)
        if Connections.executeExist(sqlConnection, query):
            query = "SELECT stock_amount FROM {TABLE} WHERE user_id = '{USER}' AND " \
                    "stock_id = '{STOCK}';".format(TABLE=stockBalancesTable, USER=userID, STOCK=stockSymbol)
            print(query)
            result = Connections.executeReadQuery(sqlConnection, query)
            print(result)
            stockHeld = result[0][0]
            if stockAmount < stockHeld:
                query = "UPDATE {TABLE} SET stock_amount = stock_amount - {RESERVE}, stock_reserved = {RESERVE} " \
                        "WHERE user_id = '{USER}' AND stock_id = '{STOCK}';".format(TABLE=stockBalancesTable, USER=userID,
                                                                                    RESERVE=stockAmount, STOCK=stockSymbol)
                print(query)
                Connections.executeQuery(sqlConnection, query)
            else:
                return {'error': "The user does not hold enough stocks to create this trigger"}
            query = "INSERT INTO {TABLE} (user_id, stock_id, type, amount) VALUES " \
                    "('{USER}', '{STOCK}', 'sell', {AMOUNT});".format(TABLE=triggersTable, USER=userID,
                                                                      STOCK=stockSymbol, AMOUNT=stockAmount)
            print(query)
            Connections.executeQuery(sqlConnection, query)
            return 1
        else:
            return {'error': "The user doesn't own this stock."}


def setSellTrigger(userID, stockSymbol, price):
    query = "SELECT EXISTS(SELECT 1 from {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'sell' LIMIT 1);".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    if Connections.executeExist(sqlConnection, query):
        query = "UPDATE {TABLE} SET trigger = {PRICE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
                "AND type = 'sell'".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol, PRICE=price)
        print(query)
        Connections.executeQuery(sqlConnection, query)
        return 1
    else:
        return {'error': "No set sell exists"}


def cancelSellTrigger(userID, stockSymbol):
    query = "DELETE FROM {TABLE} WHERE user_id = '{USER}' AND stock_id = '{STOCK}' " \
            "AND type = 'sell'".format(TABLE=triggersTable, USER=userID, STOCK=stockSymbol)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    query = "UPDATE {TABLE} SET stock_amount = stock_amount + stock_reserved, stock_reserved = 0 WHERE user_id = " \
            "'{USER}' AND stock_id = '{STOCK}';".format(TABLE=stockBalancesTable, USER=userID, STOCK=stockSymbol)
    print(query)
    Connections.executeQuery(sqlConnection, query)
    return 1


if __name__ == "__main__":
    global sqlConnection

    # Start SQL
    sqlConnection = Connections.createSQLConnection()
    Connections.checkDB(sqlConnection)

    # Create Connections
    conn = Connections.createSocket()
    print("Established Connection")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = pickle.loads(data)
        command = data["command"]

        if command == "fillAccountCache":
            print("received fillAccountCache command")
            response = fillAccountCache()
        elif command == "fillStockCache":
            print("received fillAccountCache command")
            response = fillStockCache()
        elif command == "updateAccountCache":
            print("received updateAccountCache command")
            response = updateAccountCache(data["user_id"])
        elif command == "updateStockCache":
            print("received updateStockCache command")
            response = updateStockCache(data["user_id"], data["stock_id"])

        elif command == "addFunds":
            print("received add command")
            response = addFunds(data["user_id"], data["amount"])
        elif command == "commitBuy":
            print("received commit buy command")
            response = commitBuy(data["user_id"], data["stock_id"], data["value_amount"], data["amount_of_stock"])
        elif command == "commitSell":
            print("received commit sell command")
            response = commitSell(data["user_id"], data["stock_id"], data["value_amount"], data["amount_of_stock"])

        elif command == "SET_BUY_AMOUNT":
            print("received set buy amount command")
            response = setBuyAmount(data["user_id"], data["stock_id"], data["amount_of_stock"])
        elif command == "SET_BUY_TRIGGER":
            print("received set buy trigger command")
            response = setBuyTrigger(data["user_id"], data["stock_id"], data["trigger_price"])
        elif command == "CANCEL_SET_BUY":
            print("received cancel set buy command")
            response = cancelBuyTrigger(data["user_id"], data["stock_id"])

        elif command == "SET_SELL_AMOUNT":
            print("received set sell amount command")
            response = setSellAmount(data["user_id"], data["stock_id"], data["amount_of_stock"])
        elif command == "SET_SELL_TRIGGER":
            print("received set sell trigger command")
            response = setSellTrigger(data["user_id"], data["stock_id"], data["trigger_price"])
        elif command == "CANCEL_SET_SELL":
            print("received cancel set sell command")
            response = cancelSellTrigger(data["user_id"], data["stock_id"])

        else:
            response = "Unknown command"
            print("received unknown command")
            print(data)

        if response == 1:
            conn.send("Success".encode())
        elif type(response) is dict:
            error = response["error"]
            conn.send(error.encode())
        else:
            conn.send(pickle.dumps(response))
