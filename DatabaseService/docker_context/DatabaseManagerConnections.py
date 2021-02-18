import socket
#import redis
import psycopg2
from psycopg2 import OperationalError
from time import sleep

dbmSocket = 5656
dbmHost = "dbmgr-1"

dbPort = 5432
dbName, dbUser, dbPassword = "trading-db", "daytrader", "tothemoon"


def createSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((dbmHost, dbmSocket))
    s.listen()
    conn, addr = s.accept()
    return conn


# Create a connection to the database manager
def createSQLConnection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=dbName,
            user=dbUser,
            password=dbPassword,
            host="trading-db-13",
            port=dbPort
        )
        print("Connection to PostGres Successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    connection.autocommit = True
    return connection


def checkDB(connection):
    destroyTables = "DROP TABLE IF EXISTS stocks, accounts, users, triggers CASCADE;"
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
    createTriggers = "CREATE TABLE IF NOT EXISTS triggers (" \
                     "user_id varchar(10)," \
                     "stock_id varchar(10)," \
                     "type varchar(15)," \
                     "trigger float4," \
                     "amount float4," \
                     "constraint user_id FOREIGN KEY (user_id) REFERENCES users(user_id)," \
                     "PRIMARY KEY (user_id, stock_id, type));"

    executeQuery(connection, createUser)
    executeQuery(connection, createAccounts)
    executeQuery(connection, createStocks)
    executeQuery(connection, createTriggers)


# Read helper method for the SQL server
def executeReadQuery(connection, query):
    query = query.replace('"', '')
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Write helper method for the SQL server
def executeQuery(connection, query):
    query = query.replace('"', '')
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Checks if the record exists
def executeExist(connection, query):
    query = query.replace('"', '')
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return result
