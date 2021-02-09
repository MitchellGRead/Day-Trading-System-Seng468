import socket
import redis
import psycopg2
from psycopg2 import OperationalError
from time import sleep

localHost = "localhost"
# stockHost = "quoteserver.seng.uvic.ca"
stockHost = localHost
dbmHost = localHost

redisPort = 6379
stockPort = 4444
transPort = 6666
dbmPort = 5656


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
    print("Attempting Connection to Quote Server")
    while stockSocket.connect_ex((stockHost, stockPort)) != 0:
        sleep(1)
    print("Quote Connection Started")
    return stockSocket


def createDatabaseManagerConn():
    dbmSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting Connection to DBM Server")
    while dbmSocket.connect_ex((dbmHost, dbmPort)) != 0:
        sleep(1)
    print("DBM Connection Started")
    return dbmSocket


# Starts the redis (cache) server
def startRedis():
    r = redis.Redis(host=localHost, port=redisPort, db=0)
    print("Connection to Redis Successful")
    return r
