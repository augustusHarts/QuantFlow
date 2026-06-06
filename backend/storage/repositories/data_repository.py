import orjson

from pathlib import Path
from typing import Any
from shared.models.ingestion_models import SaveRequest
from shared.enums.datalayer import DataLayer
from storage.interfaces.repository import Repository

class DataRepository(Repository):

    def __init__(
        self,
        root_dir: Path
    ):
        self.root_dir = root_dir

    def save(
        self,
        request: SaveRequest
    ) -> None:

        directory = (
            self.root_dir
            / request.layer
            / request.provider.value
        )

        directory.mkdir(
            parents=True, 
            exist_ok=True
        )

        file_path = directory / f'{request.key}.json'

        with open(
            file_path,
            'wb'
        ) as file:
            file.write(
                orjson.dumps(
                    request.payload,
                    option=orjson.OPT_INDENT_2
                )
            )

    def load(
        self,
        layer: DataLayer,
        provider: str,
        key: str
    ) -> dict[str, Any]:

        file_path = (
            self.root_dir
            / layer
            / provider
            / f"{key}.json"
        )

        with open(
            file_path,
            "rb"
        ) as file:

            return orjson.loads(
                file.read()
            )

    def exists(
        self,
        layer: DataLayer,
        provider: str,
        key: str
    ) -> bool:

        return (
            self.root_dir
            / layer
            / provider
            / f"{key}.json"
        ).exists()

    def delete(
        self,
        layer: DataLayer,
        provider: str,
        key: str
    ) -> None:

        file_path = (
            self.root_dir
            / layer
            / provider
            / f"{key}.json"
        )

        if file_path.exists():
            file_path.unlink()