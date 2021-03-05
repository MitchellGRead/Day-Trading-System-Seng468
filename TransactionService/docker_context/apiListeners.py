from sanic.log import logger

import config
from AuditHandler import AuditHandler
from ServiceLogic import ServiceLogic
from TransactionHandler import TransactionHandler


async def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        config.TRANSACTION_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT,
        loop
    )


async def initTransactionLogic(app, loop):
    logger.debug('Creating transaction handler')
    app.config['transaction'] = TransactionHandler(
        app.config['audit'],
        config.CACHE_SERVER_IP,
        config.CACHE_SERVER_PORT,
        loop
    )


async def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(app.config['transaction'])


async def closeHandlerClients(app, loop):
    logger.debug('Closing handler clients')
    await app.config['audit'].stop()
    await app.config['transaction'].stop()
