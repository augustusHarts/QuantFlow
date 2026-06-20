import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock

from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
from shared.models.pipeline_model import SaveRequest
from storage.repositories.data_repository import DataRepository


# --------------------------------------------------
# Repository Fixtures
# --------------------------------------------------

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def repository(temp_dir):
    """Create a DataRepository instance with temporary directory"""
    return DataRepository(root_dir=temp_dir)


# --------------------------------------------------
# SaveRequest Fixtures
# --------------------------------------------------

@pytest.fixture
def save_request_raw():
    """Create a SaveRequest for RAW layer"""
    return SaveRequest(
        layer=DataLayer.RAW,
        provider=DataSource.YAHOO,
        key="AAPL",
        payload={"symbol": "AAPL", "price": 150.25}
    )


@pytest.fixture
def save_request_processed():
    """Create a SaveRequest for PROCESSED layer"""
    return SaveRequest(
        layer=DataLayer.PROCESSED,
        provider=DataSource.YAHOO,
        key="MSFT",
        payload={"symbol": "MSFT", "price": 370.50}
    )


@pytest.fixture
def complex_payload():
    """Create a complex payload with nested data"""
    return {
        "symbol": "BTC-USD",
        "meta": {
            "instrumentType": "CRYPTOCURRENCY",
            "currency": "USD"
        },
        "data": [
            {"date": "2024-01-01", "open": 42000, "close": 43000},
            {"date": "2024-01-02", "open": 43000, "close": 44000}
        ]
    }
