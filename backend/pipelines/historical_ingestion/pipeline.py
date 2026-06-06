import aiohttp
import asyncio

from logging import Logger
from services.ingestion.interfaces.provider import Provider
from services.ingestion.interfaces.processor import Processor
from storage.repositories.data_repository import DataRepository
from shared.models.ingestion_models import MarketSymbol
from shared.enums.datalayer import DataLayer
from shared.models.ingestion_models import SaveRequest
from shared.enums.pipelinestatus import PipelineStatus
from shared.models.ingestion_models import IngestionResult

class HistoricalIngestion:

    def __init__(
        self,
        symbols: list[MarketSymbol],
        logger: Logger ,
        provider: Provider,
        processor: Processor,
        repository: DataRepository
    ):
        self.symbols = symbols
        self.logger = logger
        self.provider = provider
        self.processor = processor
        self.repository = repository
        self.status = PipelineStatus.PENDING

    @staticmethod
    def _get_pipeline_status(
        successful_count: int,
        failed_count: int
    ) -> PipelineStatus:

        if successful_count == 0 and failed_count > 0:
            return PipelineStatus.FAILED

        if successful_count > 0 and failed_count > 0:
            return PipelineStatus.PARTIAL_SUCCESS

        return PipelineStatus.SUCCESS

    def _persist_raw_data(
        self,
        data: dict
    ) -> None:
        
        for symbol, payload in data.items():
            self.repository.save(
                SaveRequest(
                    layer=DataLayer.RAW,
                    provider=self.provider.source,
                    key=symbol,
                    payload=payload
                )
            )    

    async def run(self) -> IngestionResult:

        if not self.symbols:
            self.logger.warning(
                "No symbols provided"
            )

            return IngestionResult(
                successful={},
                failed={}
            )

        self.status = PipelineStatus.RUNNING
        self.logger.info(
            "Ingestion Started | source=%s | status=%s | total=%d",
            self.provider.source.value,
            self.status.value,
            len(self.symbols)
        )

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.provider
                .fetch(
                    symbol=symbol.ticker, 
                    session=session
                )
                for symbol in self.symbols
            ]

            results = await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

        processed = self.processor.process(
            self.symbols, 
            results
        )

        self._persist_raw_data(processed.successful)

        self.status = self._get_pipeline_status(
            successful_count=len(processed.successful),
            failed_count=len(processed.failed)
        )

        self.logger.info(
            "Ingestion Completed | source=%s | status=%s | total=%d | successful=%d | failed=%d",
            self.provider.source.value,
            self.status.value,
            len(self.symbols),
            len(processed.successful),
            len(processed.failed)
        )

        return processed

        