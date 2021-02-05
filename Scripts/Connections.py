import socket
import redis
import psycopg2
from psycopg2 import OperationalError

localHost = "127.0.0.1"
stockHost = "quoteserver.seng.uvic.ca"

redisPort = 6379
stockPort = 4444
transPort = 6666

dbPort = 5432
dbName, dbUser, dbPassword = "TBD"


# Creates socket for Sending/Receiving from WebService
def connectWeb():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((localHost, transPort))
    s.listen()
    conn, addr = s.accept()
    print("Connected to WebService @ " + addr[0])
    return conn


# Creates a connection to the quote server.
def createQuoteConn():
    stockSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stockSocket.connect((stockHost, stockPort))
    print("Quote Connection Started")
    return stockSocket


# Create a connection to the database manager
def createDBConnection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=dbName,
            user=dbUser,
            password=dbPassword,
            host=localHost,
            port=dbPort
        )
        print("Connection to postgres successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


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
    return r
