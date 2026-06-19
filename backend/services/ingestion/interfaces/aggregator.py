from abc import ABC, abstractmethod
from typing import Any
from shared.models.ingestion_models import Result
from shared.models.ingestion_models import MarketSymbol

class Aggregator(ABC):

    @abstractmethod
    def aggregate(
        self,
        symbols: list[MarketSymbol],
        results: list[dict[str, Any] | BaseException]
    ) -> Result:
        ...