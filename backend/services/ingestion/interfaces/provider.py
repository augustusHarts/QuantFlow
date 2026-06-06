import aiohttp
from abc import ABC, abstractmethod
from shared.enums.datasource import DataSource

class Provider(ABC):

    @property
    @abstractmethod
    def source(
        self
    ) -> DataSource:
        ...

    @abstractmethod
    async def fetch(
        self,
        symbol: str,
        session: aiohttp.ClientSession
    ) -> dict:
        ...