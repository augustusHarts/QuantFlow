from abc import ABC, abstractmethod
from shared.models.preprocessing_model import PreprocessingResult, PreprocessedSymbol
from shared.models.ingestion_models import DataSource


class Aggregator(ABC):
    @abstractmethod
    def aggregate(
        self,
        symbols: list[tuple[DataSource, str]],
        results: list[PreprocessedSymbol | BaseException],
    ) -> PreprocessingResult: ...
