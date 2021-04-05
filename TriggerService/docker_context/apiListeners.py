from sanic.log import logger

import config
from AuditHandler import AuditHandler
from TriggerExecutionManager import TriggerExecutionManager
from ServiceLogic import ServiceLogic


# Before server starts ----------------------------------------------
from TriggerHandler import TriggerHandler


async def initAudit(app, loop):
    logger.debug('Creating audit handler')
    app.config['audit'] = AuditHandler(
        config.TRIGGER_SERVER_NAME,
        config.AUDIT_SERVER_IP,
        config.AUDIT_SERVER_PORT,
        loop
    )


async def initTriggerHandler(app, loop):
    logger.debug('Creating trigger handler')
    app.config['trigger_handler'] = TriggerHandler(
        app.config['audit'],
        config.DATABASE_SERVER_IP,
        config.DATABASE_SERVER_PORT,
        config.CACHE_SERVER_IP,
        config.CACHE_SERVER_PORT,
        loop
    )


async def initServiceLogic(app, loop):
    logger.debug('Creating service logic')
    app.config['logic'] = ServiceLogic(
        app.config['trigger_handler'],
        app.config['trigger_execution']
    )


# After server starts -----------------------------------------------
async def initActiveTriggers(app, loop):
    await app.config['logic'].initActiveTriggers()
# -------------------------------------------------------------------


async def initTriggerExecutionManager(app, loop):
    logger.debug('Creating trigger execution manager')
    app.config['trigger_execution'] = TriggerExecutionManager(
        app.config['audit'],
        config.CACHE_SERVER_IP,
        config.CACHE_SERVER_PORT,
        config.DATABASE_SERVER_IP,
        config.DATABASE_SERVER_PORT,
        loop
    )
# -------------------------------------------------------------------


# Before server stops -----------------------------------------------
async def closeHandlerClients(app, loop):
    await app.config['audit'].client.stop()
    await app.config['trigger_execution'].client.stop()
    await app.config['trigger_handler'].client.stop()


async def stopTriggerScheduler(app, loop):
    app.config['trigger_execution'].shutdown()
# -------------------------------------------------------------------
