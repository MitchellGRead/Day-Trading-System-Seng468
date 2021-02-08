import socket
import redis
import psycopg2
from psycopg2 import OperationalError

localHost = "127.0.0.1"
# stockHost = "quoteserver.seng.uvic.ca"
stockHost = "localhost"

redisPort = 6379
stockPort = 4444
transPort = 6666

dbPort = 5432
dbName, dbUser, dbPassword = "trading-db", "daytrader", "tothemoon"

usersTable = "users"
accountBalancesTable = "accounts"
stockBalancesTable = "stocks"



# Creates socket for Sending/Receiving from WebService
def connectWeb():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((localHost, transPort))
    s.listen()
    conn, addr = s.accept()

    print("Connected to WebService @ " + addr[0] + ":" + str(addr[1]))
    return conn


# Creates a connection to the quote server.
def createQuoteConn():
    stockSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stockSocket.connect((stockHost, stockPort))
    print("Quote Connection Started")
    return stockSocket


# Create a connection to the database manager
def createSQLConnection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=dbName,
            user=dbUser,
            password=dbPassword,
            host=localHost,
            port=dbPort
        )
        print("Connection to PostGres Successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

  
def checkDB(connection):
    destroyTables = "DROP TABLE IF EXISTS stocks, accounts, users CASCADE;"
    executeQuery(connection, destroyTables)
    createUser = "CREATE TABLE IF NOT EXISTS users (" \
                 "user_id VARCHAR(10) PRIMARY KEY);"
    createAccounts = "CREATE TABLE IF NOT EXISTS accounts (" \
                     "user_id varchar(10) PRIMARY KEY," \
                     "account_balance float4," \
                     "reserve_balance float4," \
                     "constraint user_id FOREIGN KEY (user_id) REFERENCES users(user_id));"
    createStocks = "CREATE TABLE IF NOT EXISTS stocks (" \
                   "user_id varchar(10)," \
                   "stock_id varchar(10)," \
                   "stock_amount integer," \
                   "stock_reserved integer," \
                   "constraint stock_amount check (stock_amount >= 0)," \
                   "constraint stock_reserved check (stock_reserved >= 0)," \
                   "constraint user_id FOREIGN KEY (user_id) REFERENCES users(user_id)," \
                   "PRIMARY KEY (user_id, stock_id));"
    executeQuery(connection, createUser)
    executeQuery(connection, createAccounts)
    executeQuery(connection, createStocks)

    
# Read helper method for the SQL server
def executeReadQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Write helper method for the SQL server
def executeQuery(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Checks if the record exists
def executeExist(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return result


# Starts the redis (cache) server
def startRedis():
    r = redis.Redis(host=localHost, port=redisPort, db=0)
    print("Connection to Redis Successful")
    return r
