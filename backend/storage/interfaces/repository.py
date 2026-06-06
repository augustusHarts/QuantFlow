from abc import ABC, abstractmethod
from pathlib import Path
from shared.models.ingestion_models import SaveRequest
    
class Repository(ABC):

    @abstractmethod
    def save(
        self,
        request: SaveRequest
    ) -> None:
        ...