import aiohttp
import asyncio

from logging import Logger
from shared.decorators.logging import log_stage
from services.ingestion.interfaces.provider import Provider
from services.ingestion.interfaces.processor import Processor
from services.ingestion.interfaces.preprocessor import Preprocessor
from services.ingestion.interfaces.transformation import Transformation

class HistoricalIngestion:

    def __init__(
        self,
        symbols,
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

    @log_stage('Historical Ingestion Pipeline')
    async def run(self):

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.provider
                .fetch(
                    symbol=symbol, 
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

        self.logger.info(
            "Ingestion Completed: \n\ttota_symbols: %d \n\tsuccessful_symbols: %d \n\tfailed_symbols: %d",
            len(self.symbols),
            len(processed.successful),
            len(processed.failed)
        )

        

        transformed = self.transformer.transform(processed)

        return transformed
        