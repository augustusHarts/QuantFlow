import aiohttp
import asyncio

from logging import Logger
from shared.decorators.logging import log_stage
from services.ingestion.interfaces.provider import Provider
from services.ingestion.interfaces.processor import Processor
from services.ingestion.interfaces.preprocessor import Preprocessor
from services.ingestion.interfaces.transformation import Transformation
from shared.models.ingestion_models import MarketSymbol
from shared.enums.pipelinestatus import PipelineStatus

class HistoricalIngestion:

    def __init__(
        self,
        symbols: list[MarketSymbol],
        logger: Logger ,
        provider: Provider,
        processor: Processor,
        preprocessor: Preprocessor,
        transformer: Transformation
    ):
        self.symbols = symbols
        self.logger = logger
        self.provider = provider
        self.processor = processor
        self.preprocessor = preprocessor
        self.transformer = transformer
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

    # @log_stage('Historical Ingestion Pipeline')
    async def run(self):
        self.logger.info(
            "Ingestion Started | source=%s | total=%d",
            self.provider.source.value,
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

        

        transformed = self.transformer.transform(processed)