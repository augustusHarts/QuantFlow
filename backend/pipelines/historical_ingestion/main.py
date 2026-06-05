import asyncio

from logging import Logger
from shared.utils.logger import get_logger
from pipelines.historical_ingestion.config import SYMBOLS
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.processors.yahoo_processor import YahooProcessor
from services.transformation.yahoo_transformer import YahooTransformer
from pipelines.historical_ingestion.pipeline import HistoricalIngestion

async def main():

    pipeline_logger = get_logger('Historical Ingestion Pipeline')
    provider = YahooProvider(pipeline_logger.getChild('YahooProvider'))
    processor = YahooProcessor(pipeline_logger.getChild('YahooProcessor'))
    transformer = YahooTransformer(pipeline_logger.getChild('YahooTransformer'))
    
    pipeline = HistoricalIngestion(
        SYMBOLS,
        pipeline_logger,
        provider = provider,
        processor = processor,  
        transformer = transformer
    )
    
    result = await pipeline.run()

if __name__ == '__main__':
    asyncio.run(main())