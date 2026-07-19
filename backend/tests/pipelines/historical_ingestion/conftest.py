import pytest

from unittest.mock import Mock, AsyncMock

from pipelines.ingestions.historical.pipeline import HistoricalIngestion

from shared.models.ingestion_models import MarketSymbol, Result

from shared.enums.assettype import AssetType
from shared.enums.datasource import DataSource


@pytest.fixture
def logger():
    return Mock()


@pytest.fixture
def provider():

    provider = Mock()

    provider.source = DataSource.YAHOO

    provider.fetch = AsyncMock()

    return provider


@pytest.fixture
def aggregator():
    return Mock()


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def symbols():

    return [
        MarketSymbol(ticker="AAPL", asset_type=AssetType.EQUITY),
        MarketSymbol(ticker="MSFT", asset_type=AssetType.EQUITY),
    ]


@pytest.fixture
def successful_result():

    return Result(
        successful={"AAPL": {"price": 100}, "MSFT": {"price": 200}}, failed={}
    )


@pytest.fixture
def partial_result():

    return Result(
        successful={"AAPL": {"price": 100}}, failed={"MSFT": Exception("bad")}
    )


@pytest.fixture
def failed_result():

    return Result(
        successful={}, failed={"AAPL": Exception("bad"), "MSFT": Exception("bad")}
    )


@pytest.fixture
def pipeline(logger, provider, aggregator, repository, symbols):

    return HistoricalIngestion(
        symbols=symbols,
        logger=logger,
        provider=provider,
        aggregator=aggregator,
        repository=repository,
    )
