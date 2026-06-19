import orjson

from pathlib import Path
from typing import Any
from shared.models.pipeline_model import SaveRequest
from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
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
            / request.layer.value
            / request.provider
        )

        directory.mkdir(
            parents=True, 
            exist_ok=True
        )

        if request.layer == DataLayer.RAW:
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

        elif request.layer == DataLayer.PROCESSED:
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
        provider: DataSource,
        key: str
    ) -> dict[str, Any]:

        file_path = (
            self.root_dir
            / layer.value
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

    def list_providers(
        self,
        layer: DataLayer
    ) -> list[DataSource]:

        folders = (
            self.root_dir 
            / layer
        )

        if not folders.exists():
            return []

        providers: list[DataSource] = []

        for item in folders.iterdir():
            if not item.is_dir():
                continue

            try:
                providers.append(
                    DataSource(
                        item.name
                    )
                )
                
            except ValueError:
                continue

        return providers

    def list_keys(
        self,
        layer: DataLayer,
        providers: list[DataSource]
    ) -> dict[DataSource, list[str]]:

        result = {}
        for provider in providers:
            folder = (
                self.root_dir
                / layer
                / provider.value
            )

            if not folder.exists():
                continue

            keys = [file.stem for file in folder.glob('*.json') if file.is_file()]

            result[provider.value] = keys
            
        return result
        