"""
Trigger Execution Manager will be responsible for periodically calculating if triggers are fulfilled,
sending fulfilled triggers, and pinning the cache service for price data.

There are three core data structures in the class:
1. Triggers is a dictionary with stock_symbols identifying the keys and each value being a list of BUY or SELL triggers
under said stock_symbol. Each trigger is formatted as
{'transaction_num': int, 'trigger': str, 'user_id': str, 'stock_symbol': str, 'trigger_price': double}
The trigger string can be either 'SELL_TRIGGER' or 'BUY_TRIGGER'

2. Prices is a dictionary with stock_symbols identifying the keys and each value being double representing the current price.
The format for adding a price is formatted as {'stock_symbol': str, 'price': double}

3. Results is a list of fulfilled and ready to execute triggers. This list is sent to the cache service and cleared when
successful. Otherwise it will hold onto the list on the next scheduled execution.
"""
import asyncio

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sanic.log import logger

from Client import Client


class TriggerExecutionManager:
    _EXECUTE_TRIGGERS_TIMER_SEC = 2
    _SEND_RESULTS_TIMER_SEC = 1
    _FETCH_PRICES_TIMER_SEC = 5
    _MISFIRE_TIMER_SEC = 10
    SELL = 'SELL_TRIGGER'
    BUY = 'BUY_TRIGGER'

    def __init__(self, audit, cache_ip, cache_port, dbm_ip, dbm_port, loop):
        self.audit = audit
        self.client = Client(loop)
        self.cache_url = f'http://{cache_ip}:{cache_port}'
        self.dbm_url = f'http://{dbm_ip}:{dbm_port}'
        self.scheduler = self._setupScheduler()
        self.results = []
        self.triggers = {}
        self.prices = {}

    def _setupScheduler(self):
        executor = {
            'processpool': ProcessPoolExecutor(max_workers=3)
        }
        scheduler = AsyncIOScheduler(executors=executor)
        calculateTriggersJob = scheduler.add_job(
            self._calculateTriggers,
            'interval',
            seconds=self._EXECUTE_TRIGGERS_TIMER_SEC,
            id='calculateTriggers',
            misfire_grace_time=self._MISFIRE_TIMER_SEC,
            max_instances=1,
            coalesce=False  # Run more then once
        )
        sendResultsJob = scheduler.add_job(
            self.sendResults,
            'interval',
            seconds=self._SEND_RESULTS_TIMER_SEC,
            id='sendResults',
            misfire_grace_time=self._MISFIRE_TIMER_SEC,
            max_instances=1,
            coalesce=False  # Run more then once
        )
        fetchPricesJob = scheduler.add_job(
            self.fetchPrices,
            'interval',
            seconds=self._FETCH_PRICES_TIMER_SEC,
            id='fetchPrices',
            misfire_grace_time=self._MISFIRE_TIMER_SEC,
            max_instances=3,
            coalesce=False  # Run more then once
        )
        scheduler.start()
        return scheduler

    def addTriggers(self, triggers):
        for trigger in triggers:
            self.addTrigger(trigger)

    def updatePrices(self, prices):
        for price in prices:
            self.updatePrice(price)

    def addTrigger(self, trigger):
        logger.debug(f'Adding trigger {trigger}')
        stock_symbol = trigger['stock_symbol']
        if stock_symbol in self.triggers:
            self.triggers[stock_symbol].append(trigger)
        else:
            self.triggers[stock_symbol] = [trigger]
        return "trigger added", 200

    def updatePrice(self, stock):
        logger.debug(f'Adding price for {stock}')
        symbol = stock['stock_symbol']
        self.prices[symbol] = stock['price']

    def getTrigger(self, user_id, stock_symbol, command):
        triggers = self.triggers.get(stock_symbol, [])
        if not triggers:
            return False

        for trigger in triggers:
            if trigger['user_id'] == user_id:
                if trigger['trigger'] == command:
                    return trigger
        return False

    def removeTrigger(self, trigger):
        stock_symbol = trigger['stock_symbol']
        triggers = self.triggers.get(stock_symbol, [])
        if not triggers:
            return False

        try:
            triggers.remove(trigger)
        except ValueError:
            pass
        return True

    def updateTrigger(self, old_trigger, new_trigger):
        res = self.removeTrigger(old_trigger)
        if not res:
            return

        self.addTrigger(new_trigger)

    # This is a background scheduled task
    async def sendResults(self):
        if not self.results:
            logger.debug('No trigger results available yet.')
            return

        for result in self.results:
            sendObj = {'user_id': result['user_id'], 'stock_symbol': result['stock_symbol']}
            funds = round(float(result['stock_amount'])*float(result['quoted_price']), 2)
            sendObj['funds'] = funds

            command = result['trigger']
            logger.debug(f'Sending trigger result to DBM service: {result}')

            if command == self.BUY:
                endpoint = '/triggers/execute/buy'
            elif command == self.SELL:
                endpoint = '/triggers/execute/buy'
            else:
                logger.debug(f"unknown command: {command}")
                continue

            results, status = await self.client.postRequest(f'{self.dbm_url}{endpoint}', sendObj)
            if status != 200 or results is None:
                logger.error(f'Failed to send result, keeping data.')
                continue
            logger.info('Successfully sent trigger, resetting result.')
            self.results.remove(result)

    # This is a background scheduled task
    async def fetchPrices(self):
        if not self.prices or not self.triggers:
            logger.debug('No triggers to fetch for or no prices to update')
            return

        # Only fetch stocks that have active triggers on them
        fetch_stocks = [stock for stock in self.triggers.keys() if self.triggers[stock]]

        endpoint = '/quote'
        params = {'stocks': fetch_stocks}
        results, status = await self.client.getRequest(f'{self.cache_url}{endpoint}', params)
        if status != 200 or results is None:
            logger.error('Failed fetching prices for triggers.')
            return

        logger.info('Successfully fetched trigger prices')
        self.updatePrices(results)

    def shutdown(self):
        self.scheduler.shutdown(wait=False)

    # This is a background scheduled task
    def _calculateTriggers(self):
        logger.debug('Calculating triggers')
        logger.debug(f'Current triggers: {self.triggers}')
        for stock_symbol in self.triggers:
            stock_price = self.prices.get(stock_symbol, None)
            if stock_price is None:
                logger.debug(f'No stock price available for {stock_symbol}')
                continue

            triggers = self.triggers.get(stock_symbol, [])
            if not triggers:
                logger.debug(f'No triggers available under {stock_symbol}')
                continue

            for trigger in triggers:
                trigger_type = trigger['trigger']
                if trigger_type == self.BUY:
                    self._buyTrigger(trigger, stock_price)
                elif trigger_type == self.SELL:
                    self._sellTrigger(trigger, stock_price)
                else:
                    # TODO audit event?
                    logger.error(f'An invalid trigger type has been passed. Deleting from check: {trigger}')
                    triggers.remove(trigger)

    def _buyTrigger(self, trigger, stock_price):
        trigger_price = trigger['trigger_price']
        if stock_price <= trigger_price:
            self.removeTrigger(trigger)
            trigger['quoted_price'] = stock_price
            logger.debug(f'Adding BUY trigger: {trigger}')
            self._addExecutableTrigger(trigger)

    def _sellTrigger(self, trigger, stock_price):
        trigger_price = trigger['trigger_price']
        if stock_price >= trigger_price:
            self.removeTrigger(trigger)
            trigger['quoted_price'] = stock_price
            logger.debug(f'Adding SELL trigger: {trigger}')
            self._addExecutableTrigger(trigger)

    def _addExecutableTrigger(self, trigger):
        try:
            self.results.append(trigger)
        # TODO make this better
        except asyncio.QueueFull:  # Pick it up next calculation
            pass
