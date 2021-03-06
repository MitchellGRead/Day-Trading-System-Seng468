
RUN_DEBUG = False
ACCESS_LOGS = True

WEB_SERVER_NAME = 'WebService'
WEB_SERVER_IP = 'web-1'
WEB_SERVER_PORT = 5000
WEB_SERVER_WORKERS = 3

AUDIT_SERVER_NAME = 'AuditService'
AUDIT_SERVER_IP = 'audit-1'
AUDIT_SERVER_PORT = 6500
AUDIT_SERVER_WORKERS = 1

TRIGGER_SERVER_NAME = 'TriggerService'
TRIGGER_SERVER_IP = 'trigger-1'
TRIGGER_SERVER_PORT = 7000
TRIGGER_SERVICE_WORKERS = 1

TRANSACTION_SERVER_NAME = 'TransactionService'
TRANSACTION_SERVER_IP = 'trsrvr-1'
TRANSACTION_SERVER_PORT = 6666
TRANSACTION_SERVICE_WORKERS = 3

DATABASE_SERVER_NAME = "DatabaseService"
DATABASE_SERVER_IP = 'dbmgr-1'
DATABASE_SERVER_PORT = 5656
DATABASE_SERVICE_WORKERS = 1

CACHE_SERVER_NAME = "CacheService"
CACHE_SERVER_IP = 'cache-1'
CACHE_SERVER_PORT = 9999
CACHE_REDIS_IP = 'redis-1'
CACHE_REDIS_PORT = 6379
CACHE_SERVICE_WORKERS = 3

LEGACY_STOCK_SERVER_NAME = 'StockService'
DUMMY_STOCK_SERVER_IP = 'dummy-stock-1'
DUMMY_STOCK_SERVER_PORT = 4444
LEGACY_STOCK_SERVER_IP = '192.168.4.2'
LEGACY_STOCK_SERVER_PORT = 4444
