import pickle
import DatabaseManagerConnections as Connections

usersTable = "users"
accountBalancesTable = "accounts"
stockBalancesTable = "stocks"


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


if __name__ == "__main__":
    global sqlConnection

    # Start SQL
    sqlConnection = Connections.createSQLConnection()
    Connections.checkDB(sqlConnection)

    # Create Connections
    conn = Connections.createSocket()
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
            print("received unknown command")
            print(data)

        if response == 1:
            conn.send("Success".encode())
        else:
            conn.send(pickle.dumps(response))
