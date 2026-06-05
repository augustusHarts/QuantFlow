from abc import ABC, abstractmethod
import aiohttp

class Provider(ABC):

    @abstractmethod
    async def fetch(
        self,
        symbol: str,
        session: aiohttp.ClientSession
    ) -> dict:
        ...