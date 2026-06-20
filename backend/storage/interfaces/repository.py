from abc import ABC, abstractmethod
from shared.models.pipeline_model import SaveRequest
from typing import Any
from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource


class Repository(ABC):
    @abstractmethod
    def save(self, request: SaveRequest) -> None: ...

    @abstractmethod
    def load(
        self, layer: DataLayer, provider: DataSource, key: str
    ) -> dict[str, Any]: ...

    @abstractmethod
    def exists(self, layer: DataLayer, provider: str, key: str) -> bool: ...

    @abstractmethod
    def delete(self, layer: DataLayer, provider: str, key: str) -> None: ...

    @abstractmethod
    def list_providers(self, layer: DataLayer) -> list[DataSource]: ...

    @abstractmethod
    def list_keys(
        self, layer: DataLayer, providers: list[DataSource]
    ) -> dict[DataSource, list[str]]: ...
