import asyncio
import aiohttp
import logging 

from shared.config.ingestion_config import BASE_URL, YAHOO_INTERVAL, YAHOO_RANGE, API_TIMEOUT
from services.ingestion.interfaces.provider import Provider
from shared.exceptions.ingestion_exceptions import (
    YahooFetchError,
    YahooRateLimitError,
    YahooInvalidResponseError
)

class YahooProvider(Provider):

    def __init__(
        self,
        logger: logging.Logger
    ):
        self.base_url = BASE_URL
        self.range = YAHOO_RANGE
        self.interval = YAHOO_INTERVAL
        self.timeout = API_TIMEOUT
        self.logger = logger

    async def fetch(
        self, 
        symbol: str, 
        session: aiohttp.ClientSession
    ):

        url = f'{self.base_url}/{symbol}'
        params = {
            'range': self.range,
            'interval': self.interval
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110'}
        retries = 3
        base_backoff = 2

        for attempt in range(1, retries+1):
            
            try:
                async with session.get(
                    url, 
                    params=params, 
                    headers=headers, 
                    timeout=self.timeout
                ) as response:
                    
                    if response.status == 429:
                        self.logger.error('Ingestion Stage: Rate Limit Exceeded (429)')
                        raise YahooRateLimitError() 
                    
                    response.raise_for_status()
                    data = await response.json()

                    chart = data.get('chart', {})

                    if not chart.get('result') or chart.get('error') is not None :
                        self.logger.error(
                            'invalid_response',
                            extra={
                                'symbol': symbol
                            }
                        )
                        raise YahooInvalidResponseError()
                    
                    return data

            except asyncio.TimeoutError as e:
                self.logger.error(
                    'request_timeout',
                    extra={
                        'error': str(e)
                    }
                )

                if attempt < retries:
                    self.logger.info(
                        'retry_scheduled', 
                        extra={
                            'attempts': attempt,
                            'delay_seconds': base_backoff ** attempt
                        }
                    ) 
                    await asyncio.sleep(base_backoff ** attempt)

                else:
                    self.logger.error('Ingestion Stage: Max retries reached')
                    raise 

            except YahooInvalidResponseError:
                self.logger.error('Data from Yahoo Finance API is invalid')
                raise 

        raise YahooFetchError()