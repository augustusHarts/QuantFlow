from pipelines.orchestration.master_pipeline import MasterPipeline
from pipelines.historical_ingestion.pipeline import HistoricalIngestion
from shared.utils.logger import get_logger
from pipelines.historical_ingestion.config import SYMBOLS
from shared.config.storage_config import DATASET_DIR
from shared.config.ingestion_config import (
    BASE_URL,
    YAHOO_RANGE,
    YAHOO_INTERVAL,
    API_TIMEOUT
)
import asyncio
from shared.models.ingestion_models import YahooConfig
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator
from services.ingestion.aggregators.yahoo_aggregator import YahooAggregator
from storage.repositories.data_repository import DataRepository
from shared.enums.datasource import DataSource

async def main():

    master_logger = get_logger('QuantFlow Pipeline')

    yahoo_config = YahooConfig(
        base_url=BASE_URL,
        range=YAHOO_RANGE,
        interval=YAHOO_INTERVAL,
        timeout=API_TIMEOUT,
        source=DataSource.YAHOO
    )
    
    provider = YahooProvider(
        logger=master_logger.getChild('YahooProvider'),
        validator=YahooValidator(),
        config=yahoo_config
    )
    aggregator = YahooAggregator(master_logger.getChild('YahooAggregator'))
    repository = DataRepository(root_dir=DATASET_DIR)
    
    historical_pipeline = HistoricalIngestion(
        SYMBOLS,
        logger = master_logger,
        provider = provider,
        aggregator = aggregator,  
        repository=repository
    )
    
    pipeline = MasterPipeline(
        master_logger,
        historical_pipeline
    )
    await pipeline.run()

if __name__ == '__main__':
    asyncio.run(main())