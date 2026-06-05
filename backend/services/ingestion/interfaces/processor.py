from abc import ABC, abstractmethod
from typing import Any
from shared.models.ingestion_models import IngestionResult

class Processor(ABC):

    @abstractmethod
    def process(
        self,
        symbols: list[str],
        results: list[dict[str, Any] | BaseException]
    ) -> IngestionResult:
        ...