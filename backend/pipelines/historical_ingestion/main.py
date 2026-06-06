import asyncio

from shared.utils.logger import get_logger
from pipelines.historical_ingestion.config import SYMBOLS
from shared.config.ingestion_config import (
    BASE_URL,
    YAHOO_RANGE,
    YAHOO_INTERVAL,
    API_TIMEOUT
)
from shared.models.ingestion_models import YahooConfig
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator
from services.ingestion.processors.yahoo_processor import YahooProcessor
from services.preprocessing.yahoo_preprocessor import YahooPreprocessor
from services.transformation.yahoo_transformer import YahooTransformer
from pipelines.historical_ingestion.pipeline import HistoricalIngestion

async def main():

    pipeline_logger = get_logger('Historical Ingestion Pipeline')

    yahoo_config = YahooConfig(
        base_url=BASE_URL,
        range=YAHOO_RANGE,
        interval=YAHOO_INTERVAL,
        timeout=API_TIMEOUT
    )
    
    provider = YahooProvider(
        logger=pipeline_logger.getChild('YahooProvider'),
        validator=YahooValidator(),
        config=yahoo_config
    )
    processor = YahooProcessor(pipeline_logger.getChild('YahooProcessor'))
    preprocessor = YahooPreprocessor(pipeline_logger.getChild('YahooPreprocessor'))
    transformer = YahooTransformer(pipeline_logger.getChild('YahooTransformer'))
    
    pipeline = HistoricalIngestion(
        SYMBOLS,
        pipeline_logger,
        provider = provider,
        processor = processor,  
        preprocessor=preprocessor,
        transformer = transformer
    )
    
    await pipeline.run()

if __name__ == '__main__':
    asyncio.run(main())