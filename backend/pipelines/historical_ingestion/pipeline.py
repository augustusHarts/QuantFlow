import aiohttp
import asyncio
from typing import Any
import json

from backend.shared.utils.logger import get_logger
from shared.config.ingestion_config import RAW_DIR
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.processor.yahoo_processor import YahooProcessor
from services.transformation.yahoo_transformer import YahooTransformer

class HisotricalIngestion:

    #--------------------------------------------------------------
    def __init__(
        self, 
        symbols: list[str]
    ):
        self.symbols = symbols
        self.logger = get_logger(
            name="market_platform.ingestion",
            log_file="ingestion.log",
            pipeline_id="daily_ingestion_20260528",
            job_id="job_001"
        )
        self.yahoo_provider = YahooProvider(self.logger)
        self.yahoo_processor = YahooProcessor(self.logger)
        self.yahoo_transformer = YahooTransformer(self.logger)
    #--------------------------------------------------------------

    #--------------------------------------------------------------
    async def run_ingestion(self) -> list[Any | BaseException]:
        async with aiohttp.ClientSession() as session:

            tasks = [
                self.yahoo_provider
                .fetch_price(
                    symbol, 
                    session
                )
                for symbol in self.symbols
            ]

            results = await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

        return results
    #--------------------------------------------------------------

    # ! --------------------------------------------------------------
    def dev_save_raw(
        self,
        successful: dict
    ):
        for symbol, data in successful.items():
            file_path = RAW_DIR / f'{symbol}.json'

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    # ! --------------------------------------------------------------
        
    #--------------------------------------------------------------
    async def run_pipeline(self):
        
        self.logger.info(
            'ingestion_pipeline_started',
            extra={
                'symbol':len(self.symbols)
            }
        )
        
        results = await self.run_ingestion()

        raw_data = self.yahoo_processor.process_results(self.symbols, results)

        self.dev_save_raw(raw_data.successful)

        transfomation = self.yahoo_transformer.transform(raw_data.successful)

        self.logger.info(
            'ingestion_pipeline_completed',
            extra={
                'total_symbols': len(self.symbols),
                'successful': len(raw_data.successful),
                'failed': len(raw_data.failed)
            }
        )
    #--------------------------------------------------------------