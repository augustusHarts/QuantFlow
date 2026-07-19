import asyncio

from shared.utils.logger import get_logger
from pipelines.ingestions.historical.config import SYMBOLS
from shared.config.storage_config import DATASET_DIR
from shared.config.ingestion_config import (
    BASE_URL,
    YAHOO_RANGE,
    YAHOO_INTERVAL,
    API_TIMEOUT,
)
from shared.models.ingestion_models import YahooConfig
from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator
from services.ingestion.aggregators.yahoo_aggregator import YahooAggregator
from storage.repositories.data_repository import DataRepository
from pipelines.ingestions.historical.pipeline import HistoricalIngestion
from shared.enums.datasource import DataSource


async def main():

    pipeline_logger = get_logger("Historical Ingestion Pipeline")

    yahoo_config = YahooConfig(
        base_url=BASE_URL,
        range=YAHOO_RANGE,
        interval=YAHOO_INTERVAL,
        timeout=API_TIMEOUT,
        source=DataSource.YAHOO,
    )

    provider = YahooProvider(
        logger=pipeline_logger.getChild("YahooProvider"),
        validator=YahooValidator(),
        config=yahoo_config,
    )
    aggregator = YahooAggregator(pipeline_logger.getChild("YahooAggregator"))
    repository = DataRepository(root_dir=DATASET_DIR)

    pipeline = HistoricalIngestion(
        SYMBOLS,
        logger=pipeline_logger,
        provider=provider,
        aggregator=aggregator,
        repository=repository,
    )

    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(main())
