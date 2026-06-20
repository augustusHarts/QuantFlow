import logging
import pytest

from unittest.mock import Mock
from aiohttp import ClientTimeout

from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator

from shared.models.ingestion_models import YahooConfig
from shared.enums.datasource import DataSource


@pytest.fixture
def logger():
    return logging.getLogger("test")


@pytest.fixture
def validator():
    return Mock(spec=YahooValidator)


@pytest.fixture
def config():

    return YahooConfig(
        base_url="https://test.yahoo.com",
        range="1y",
        interval="1d",
        timeout=ClientTimeout(total=20),
        source=DataSource.YAHOO,
    )


@pytest.fixture
def provider(logger, validator, config):
    return YahooProvider(logger=logger, validator=validator, config=config)
