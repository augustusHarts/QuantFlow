import asyncio
import aiohttp
import logging 
from typing import Any, Final
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from shared.config.ingestion_config import DEFAULT_HEADERS 
from services.ingestion.interfaces.provider import Provider
from services.ingestion.validators.yahoo_validator import YahooValidator
from shared.models.ingestion_models import YahooConfig
from shared.exceptions.ingestion_exceptions import (
    YahooRateLimitError
)

class YahooProvider(Provider):

    def __init__(
        self,
        logger: logging.Logger,
        validator: YahooValidator,
        config: YahooConfig
    ):
        self.logger = logger
        self.validator = validator
        self.config = config

    def _build_params(self) -> dict[str, str]:
        return {
            'range': self.config.range,
            'interval': self.config.interval
        }

    def _build_headers(self) -> dict[str, str]:
        return DEFAULT_HEADERS.copy()
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10
        ),
        retry=retry_if_exception_type(
           (
               asyncio.TimeoutError,
                aiohttp.ClientError,
            )
        ),
        reraise=True
    )
    async def fetch(
        self, 
        symbol: str, 
        session: aiohttp.ClientSession
    ) -> dict[str, Any]:

        url = f'{self.config.base_url}/{symbol}'

        async with session.get(
            url,
            params=self._build_params(),
            headers=self._build_headers(),
            timeout=self.config.timeout
        ) as response:

            if response.status == 429:
                raise YahooRateLimitError() 

            response.raise_for_status()

            data = await response.json()

            self.validator.validate(data)

            return data