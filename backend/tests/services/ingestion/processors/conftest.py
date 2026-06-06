import pytest
import logging

from services.ingestion.processors.yahoo_processor import YahooProcessor


@pytest.fixture
def logger():
    return logging.getLogger("test")


@pytest.fixture
def processor(logger):
    return YahooProcessor(logger)