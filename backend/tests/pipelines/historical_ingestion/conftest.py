import logging
import pytest

from unittest.mock import Mock

from pipelines.historical_ingestion.pipeline import (
    HistoricalIngestion
)

@pytest.fixture
def logger():
    return logging.getLogger("test")

@pytest.fixture
def provider():
    return Mock()

@pytest.fixture
def processor():
    return Mock()

@pytest.fixture
def transformer():
    return Mock()

@pytest.fixture
def symbols():
    return [
        "AAPL",
        "MSFT",
        "GOOG"
    ]

@pytest.fixture
def pipeline(
    symbols,
    logger,
    provider,
    processor,
    transformer
):
    return HistoricalIngestion(
        symbols=symbols,
        logger=logger,
        provider=provider,
        processor=processor,
        transformer=transformer
    )