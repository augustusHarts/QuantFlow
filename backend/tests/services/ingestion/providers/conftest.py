import logging
import pytest
from unittest.mock import Mock

from services.ingestion.providers.yahoo_provider import YahooProvider
from services.ingestion.validators.yahoo_validator import YahooValidator


@pytest.fixture
def logger():
    return logging.getLogger("test")


@pytest.fixture
def validator():
    return Mock(spec=YahooValidator)


@pytest.fixture
def provider(
    logger,
    validator
):
    return YahooProvider(
        logger=logger,
        validator=validator
    )