import logging

import aiohttp
from aiohttp import ClientResponseError

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class Client:

    SERVICE_UNAVAILABLE_STATUS = 503

    def __init__(self, loop):
        self.client = aiohttp.ClientSession(loop=loop)
        self.loop = loop

    async def getJson(self, response):
        result = None
        try:
            result = await response.json()
        except ClientResponseError:
            logging.error(f'Invalid content type received, expected json but got {response.headers["Content-Type"]}')
        except Exception:
            logging.exception('Unknown exception occurred while retrieving response data.')
        return result, response.status

    def resetConnection(self):
        self.client = aiohttp.ClientSession(loop=self.loop)

    async def getRequest(self, url, params=None, max_retry=5):
        if not params:
            params = {}

        result = None
        status = self.SERVICE_UNAVAILABLE_STATUS
        retry_count = 1
        while retry_count <= max_retry:
            try:
                async with self.client.get(url, params=params) as resp:
                    result, status = await self.getJson(resp)

                if result is None:
                    logging.error(f'No result received from {url}. Retry {retry_count} of {max_retry}')
                    retry_count += 1
                else:
                    break
            except ConnectionResetError:
                logging.error(f'Connection reset on get request - {url}. Retry {retry_count} of {max_retry}')
                retry_count += 1
                self.resetConnection()
            except Exception:
                logging.exception(f'Unknown exception occurred on get request {url}. Retry {retry_count} of {max_retry}')
                retry_count += 1
                self.resetConnection()

        return result, status

    async def postRequest(self, url, json, max_retry=5):
        result = None
        status = self.SERVICE_UNAVAILABLE_STATUS
        retry_count = 1
        while retry_count <= max_retry:
            try:
                async with self.client.post(url, json=json) as resp:
                    result, status = await self.getJson(resp)

                if result is None:
                    logging.error(f'No result received from {url}. Retry {retry_count} of {max_retry}')
                    retry_count += 1
                else:
                    break
            except ConnectionResetError:
                logging.error(f'Connection reset on post request - {url}. Retry {retry_count} of {max_retry}')
                retry_count += 1
                self.resetConnection()
            except Exception:
                logging.exception(f'Unknown exception occurred on get request {url}. Retry {retry_count} of {max_retry}')
                retry_count += 1
                self.resetConnection()

        return result, status

    async def stop(self):
        await self.client.close()

