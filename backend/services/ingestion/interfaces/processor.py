from abc import ABC, abstractmethod
from typing import Any
from shared.models.ingestion_models import IngestionResult
from shared.models.ingestion_models import MarketSymbol

class Processor(ABC):

    @abstractmethod
    def process(
        self,
        symbols: list[MarketSymbol],
        results: list[dict[str, Any] | BaseException]
    ) -> IngestionResult:
        ...