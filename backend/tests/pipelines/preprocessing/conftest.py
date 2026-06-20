import pytest
from unittest.mock import Mock
from datetime import datetime, UTC

from shared.enums.datasource import DataSource
from shared.enums.assettype import AssetType
from shared.models.preprocessing_model import (
    PriceRecord,
    PreprocessedSymbol,
    MetaData,
    PreprocessingResult,
)
from pipelines.preprocessing.pipeline import PreprocessingPipeline


# --------------------------------------------------
# Logger Fixtures
# --------------------------------------------------
@pytest.fixture
def mock_logger():
    """Create a mock logger"""
    return Mock()


# --------------------------------------------------
# Repository Fixtures
# --------------------------------------------------
@pytest.fixture
def mock_repository():
    """Create a mock data repository"""
    return Mock()


# --------------------------------------------------
# Preprocessor Fixtures
# --------------------------------------------------
@pytest.fixture
def mock_preprocessor():
    """Create a mock preprocessor"""
    return Mock()


# --------------------------------------------------
# Aggregator Fixtures
# --------------------------------------------------
@pytest.fixture
def mock_aggregator():
    """Create a mock aggregator"""
    return Mock()


# --------------------------------------------------
# Pipeline Fixtures
# --------------------------------------------------
@pytest.fixture
def pipeline(mock_logger, mock_preprocessor, mock_aggregator, mock_repository):
    """Create a PreprocessingPipeline instance"""
    return PreprocessingPipeline(
        logger=mock_logger,
        preprocessor=mock_preprocessor,
        aggregator=mock_aggregator,
        repository=mock_repository,
    )


# --------------------------------------------------
# Data Fixtures
# --------------------------------------------------
@pytest.fixture
def valid_metadata():
    """Create valid metadata"""
    return MetaData(
        symbol="AAPL",
        asset_type=AssetType.EQUITY,
        currency="USD",
        exchange="NASDAQ",
        timezone="America/New_York",
        source=DataSource.YAHOO,
    )


@pytest.fixture
def valid_price_records():
    """Create valid price records"""
    return [
        PriceRecord(
            timestamp=datetime(2023, 1, 1, tzinfo=UTC),
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        ),
        PriceRecord(
            timestamp=datetime(2023, 1, 2, tzinfo=UTC),
            open=101.0,
            low=99.0,
            high=103.0,
            close=102.0,
            adj_close=102.0,
            volume=1200000,
        ),
    ]


@pytest.fixture
def valid_preprocessed_symbol(valid_metadata, valid_price_records):
    """Create a valid preprocessed symbol"""
    return PreprocessedSymbol(meta=valid_metadata, records=valid_price_records)


@pytest.fixture
def empty_keys():
    """Create empty keys dictionary"""
    return {}


@pytest.fixture
def single_provider_keys():
    """Create keys with single provider"""
    return {DataSource.YAHOO: ["AAPL", "MSFT"]}


@pytest.fixture
def multiple_provider_keys():
    """Create keys with multiple providers"""
    return {DataSource.YAHOO: ["AAPL", "MSFT"], DataSource.YAHOO: ["GOOGL"]}


@pytest.fixture
def raw_yahoo_data():
    """Create raw Yahoo data"""
    return {
        "chart": {
            "result": [
                {
                    "meta": {
                        "symbol": "AAPL",
                        "instrumentType": "EQUITY",
                        "currency": "USD",
                        "exchangeName": "NASDAQ",
                        "timezone": "America/New_York",
                    },
                    "timestamp": [1672531200],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0],
                                "low": [98.0],
                                "high": [102.0],
                                "close": [101.0],
                                "volume": [1000000],
                            }
                        ],
                        "adjclose": [{"adjclose": [101.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def preprocessing_result_all_success(valid_preprocessed_symbol):
    """Create preprocessing result with all successes"""
    meta_msft = MetaData(
        symbol="MSFT",
        asset_type=AssetType.EQUITY,
        currency="USD",
        exchange="NASDAQ",
        timezone="America/New_York",
        source=DataSource.YAHOO,
    )
    symbol_msft = PreprocessedSymbol(
        meta=meta_msft, records=valid_preprocessed_symbol.records
    )

    return PreprocessingResult(
        successful={
            (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
            (DataSource.YAHOO, "MSFT"): symbol_msft,
        },
        failed={},
    )


@pytest.fixture
def preprocessing_result_all_failed():
    """Create preprocessing result with all failures"""
    return PreprocessingResult(
        successful={},
        failed={
            (DataSource.YAHOO, "AAPL"): ValueError("Processing failed"),
            (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
        },
    )


@pytest.fixture
def preprocessing_result_mixed(valid_preprocessed_symbol):
    """Create preprocessing result with mixed results"""
    return PreprocessingResult(
        successful={
            (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
        },
        failed={
            (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
        },
    )
