from shared.enums.datalayer import DataLayer
from shared.models.pipeline_model import SaveRequest
from shared.enums.pipelinestatus import PipelineStatus
from storage.repositories.data_repository import DataRepository
from services.ingestion.interfaces.provider import Provider


def persist_raw_data(
    repository: DataRepository, provider: Provider, data: dict
) -> None:

    for symbol, payload in data.items():
        repository.save(
            SaveRequest(
                layer=DataLayer.RAW,
                provider=provider.source,
                key=symbol,
                payload=payload,
            )
        )


def get_pipeline_status(successful_count: int, failed_count: int) -> PipelineStatus:

    if successful_count == 0 and failed_count > 0:
        return PipelineStatus.FAILED

    if successful_count > 0 and failed_count > 0:
        return PipelineStatus.PARTIAL_SUCCESS

    return PipelineStatus.SUCCESS
