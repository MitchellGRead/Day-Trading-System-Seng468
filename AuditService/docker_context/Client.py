import asyncio

import aiohttp
from aiohttp import ClientResponseError
from sanic.log import logger


class Client:

    SERVICE_UNAVAILABLE_STATUS = 503

    def __init__(self, loop):
        self.client = aiohttp.ClientSession(loop=loop)
        self.loop = loop

    async def getResult(self, response, contentType='json'):
        result = None
        try:
            if contentType == 'json':
                result = await response.json()
            elif contentType == 'text':
                result = await response.read()
        except ClientResponseError:
            logger.error(f'Invalid content type received, expected json but got {response.headers["Content-Type"]}')
        except Exception:
            logger.exception('Unknown exception occurred while retrieving response data.')
        return result, response.status

    async def resetConnection(self):
        await self.stop()
        self.client = aiohttp.ClientSession(loop=self.loop)

    async def getRequest(self, url, params=None, contentType='json', max_retry=5):
        if not params:
            params = {}

        result = None
        status = self.SERVICE_UNAVAILABLE_STATUS
        retry_count = 1
        while retry_count <= max_retry:
            try:
                async with self.client.get(url, params=params) as resp:
                    if contentType == 'json':
                        result, status = await self.getResult(resp)
                    elif contentType == 'text':
                        result, status = await self.getResult(resp, contentType)

                if result is None:
                    logger.error(f'No result received from {url}. Retry {retry_count} of {max_retry}')
                else:
                    return result, status
            except ConnectionResetError:
                logger.error(f'Connection reset on get request - {url}. Retry {retry_count} of {max_retry}')
            except Exception:
                logger.exception(f'Unknown exception occurred on get request {url}. Retry {retry_count} of {max_retry}')

            # Only gets here on failure
            retry_count += 1
            await self.resetConnection()
            await asyncio.sleep(0.3)

        # (None, some status)
        return result, status

    async def postRequest(self, url, json, max_retry=5):
        result = None
        status = self.SERVICE_UNAVAILABLE_STATUS
        retry_count = 1
        while retry_count <= max_retry:
            try:
                async with self.client.post(url, json=json) as resp:
                    result, status = await self.getResult(resp)

                if result is None:
                    logger.error(f'No result received from {url}. Retry {retry_count} of {max_retry}')
                else:
                    return result, status
            except ConnectionResetError:
                logger.error(f'Connection reset on post request - {url}. Retry {retry_count} of {max_retry}')
            except Exception:
                logger.exception(f'Unknown exception occurred on get request {url}. Retry {retry_count} of {max_retry}')

            # Only gets here on failure
            retry_count += 1
            await self.resetConnection()
            await asyncio.sleep(0.3)

        # (None, some status)
        return result, status

    async def stop(self):
        await self.client.close()

