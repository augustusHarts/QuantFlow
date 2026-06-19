from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
from shared.enums.pipelinestatus import PipelineStatus
from storage.repositories.data_repository import DataRepository
from shared.models.pipeline_model import SaveRequest

def persist_processed_data(
        repository: DataRepository,
        data: dict
    ) -> None:
        
        for (provider, symbol), payload in data.items():
            repository.save(
                SaveRequest(
                    layer=DataLayer.PROCESSED,
                    provider=provider,
                    key=symbol,
                    payload=payload
                )
            )

def get_pipeline_status(
    successful_count: int,
    failed_count: int
) -> PipelineStatus:

    if successful_count == 0 and failed_count > 0:
        return PipelineStatus.FAILED

    if successful_count > 0 and failed_count > 0:
        return PipelineStatus.PARTIAL_SUCCESS

    return PipelineStatus.SUCCESS

def get_key_list(
    repository: DataRepository,
    layer: DataLayer
) -> dict[DataSource, list[str]] :

    providers = repository.list_providers(layer)
    return repository.list_keys(layer, providers)