import aiohttp
import asyncio

from logging import Logger
from services.ingestion.interfaces.provider import Provider
from services.ingestion.interfaces.aggregator import Aggregator
from storage.repositories.data_repository import DataRepository
from shared.models.ingestion_models import MarketSymbol
from pipelines.ingestions.historical.tasks import persist_raw_data, get_pipeline_status
from shared.enums.pipelinestatus import PipelineStatus
from shared.models.ingestion_models import Result


class HistoricalIngestion:
    def __init__(
        self,
        symbols: list[MarketSymbol],
        logger: Logger,
        provider: Provider,
        aggregator: Aggregator,
        repository: DataRepository,
    ):
        self.symbols = symbols
        self.logger = logger
        self.provider = provider
        self.aggregator = aggregator
        self.repository = repository
        self.status = PipelineStatus.PENDING

    async def run(self) -> Result:

        if not self.symbols:
            self.logger.warning("No symbols provided")

            return Result(successful={}, failed={})

        self.status = PipelineStatus.RUNNING
        self.logger.info(
            "Ingestion Started | source=%s | status=%s | total=%d",
            self.provider.source.value,
            self.status.value,
            len(self.symbols),
        )

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.provider.fetch(symbol=symbol.ticker, session=session)
                for symbol in self.symbols
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

        aggregated = self.aggregator.aggregate(self.symbols, results)

        persist_raw_data(self.repository, self.provider, data=aggregated.successful)

        self.status = get_pipeline_status(
            successful_count=len(aggregated.successful),
            failed_count=len(aggregated.failed),
        )

        self.logger.info(
            "Ingestion Completed | source=%s | status=%s | total=%d | successful=%d | failed=%d",
            self.provider.source.value,
            self.status.value,
            len(self.symbols),
            len(aggregated.successful),
            len(aggregated.failed),
        )

        return aggregated
