import socket
import redis
from time import sleep

serviceName = 'TransactionService'

transHost = 'trsrvr-1'
# stockHost = "192.168.4.2"
stockHost = 'dummy-stock-1'
auditHost = "audit-1"
dbmHost = 'dbmgr-1'
redisHost = "redis-1"

redisPort = 6379
stockPort = 4444
transPort = 6666
auditPort = 6500
dbmPort = 5656


# Creates socket for Sending/Receiving from WebService
def connectWeb():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((transHost, transPort))
    s.listen()
    conn, addr = s.accept()

    print("Connected to WebService @ " + addr[0] + ":" + str(addr[1]))
    return conn


# Creates socket for Sending/Receiving from AuditService
def connectAudit():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting Connection to Audit Server")
    while s.connect_ex((auditHost, auditPort)) != 0:
        sleep(1)
    print("Quote Connection Started")
    return s


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
    r = redis.Redis(host=redisHost, port=redisPort, db=0)
    print("Connection to Redis Successful")
    return r
