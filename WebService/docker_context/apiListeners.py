from sanic.log import logger

import config
from ServiceLogic import ServiceLogic
from AuditHandler import AuditHandler
from TransactionHandler import TransactionHandler

def initAudit(app, loop):
    logger.debug('Creating handlers handler')
    app.config['audit'] = AuditHandler(
        config.WEB_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT,
        loop
    )


def initTransaction(app, loop):
    logger.debug('Creating transaction handler')
    app.config['transaction'] = TransactionHandler(
        config.TRANSACTION_SERVER_IP,
        config.TRANSACTION_SERVER_PORT,
        loop
    )


def initServiceLogic(app, loop):
    logger.debug('Creating api logic handler')
    app.config['logic'] = ServiceLogic(
        app.config['audit'],
        app.config['transaction']
    )


async def closeHandlerClients(app, loop):
    logger.debug('Closing handler clients')
    await app.config['audit'].closeClient()
    await app.config['transaction'].closeClient()
