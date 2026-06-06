import pytest
import logging

from services.ingestion.processors.yahoo_processor import YahooProcessor
from shared.models.ingestion_models import MarketSymbol
from shared.enums.assettype import AssetType


@pytest.fixture
def logger():
    return logging.getLogger("test")


@pytest.fixture
def processor(logger):
    return YahooProcessor(logger)

@pytest.fixture
def symbols():

    return [
        MarketSymbol(
            ticker="AAPL",
            asset_type=AssetType.EQUITY
        ),
        MarketSymbol(
            ticker="MSFT",
            asset_type=AssetType.EQUITY
        )
    ]