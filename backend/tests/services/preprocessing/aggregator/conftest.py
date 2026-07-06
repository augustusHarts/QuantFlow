import pytest
from datetime import datetime, UTC
from unittest.mock import Mock

from shared.models.preprocessing_model import PriceRecord, PreprocessedSymbol, MetaData
from shared.enums.assettype import AssetType
from shared.enums.datasource import DataSource
from backend.services.preprocessing.validators.preprocessor_validator import (
    PreprocessorValidator,
)
from services.preprocessing.aggregators.preprocessor_aggregator import (
    PreprocessorAggregator,
)
from services.preprocessing.preprocessors.yahoo_preprocessor import YahooPreprocessor


# --------------------------------------------------
# Logger Fixtures
# --------------------------------------------------
@pytest.fixture
def mock_logger():
    """Create a mock logger for testing"""
    return Mock()


# --------------------------------------------------
# Validator Fixtures
# --------------------------------------------------
@pytest.fixture
def validator():
    """Create a real PreprocessorValidator instance"""
    return PreprocessorValidator()


# --------------------------------------------------
# Aggregator Fixtures
# --------------------------------------------------
@pytest.fixture
def aggregator(mock_logger):
    """Create a PreprocessorAggregator instance"""
    return PreprocessorAggregator(logger=mock_logger)


# --------------------------------------------------
# Preprocessor Fixtures
# --------------------------------------------------
@pytest.fixture
def yahoo_preprocessor(mock_logger, validator):
    """Create a YahooPreprocessor instance"""
    return YahooPreprocessor(logger=mock_logger, validator=validator)


# --------------------------------------------------
# Data Fixtures
# --------------------------------------------------
@pytest.fixture
def valid_metadata():
    """Create valid MetaData"""
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
    """Create valid PriceRecord list"""
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
        PriceRecord(
            timestamp=datetime(2023, 1, 3, tzinfo=UTC),
            open=102.0,
            low=100.0,
            high=104.0,
            close=103.0,
            adj_close=103.0,
            volume=1100000,
        ),
    ]


@pytest.fixture
def valid_preprocessed_symbol(valid_metadata, valid_price_records):
    """Create a valid PreprocessedSymbol"""
    return PreprocessedSymbol(meta=valid_metadata, prices=valid_price_records)


@pytest.fixture
def valid_yahoo_data():
    """Create valid Yahoo API response data"""
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
                    "timestamp": [1672531200, 1672617600, 1672704000],  # Jan 1-3, 2023
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0, 101.0, 102.0],
                                "low": [98.0, 99.0, 100.0],
                                "high": [102.0, 103.0, 104.0],
                                "close": [101.0, 102.0, 103.0],
                                "volume": [1000000, 1200000, 1100000],
                            }
                        ],
                        "adjclose": [{"adjclose": [101.0, 102.0, 103.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def yahoo_data_with_none_values():
    """Create Yahoo data with None values in OHLC"""
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
                    "timestamp": [1672531200, 1672617600, 1672704000],
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0, None, 102.0],
                                "low": [98.0, 99.0, 100.0],
                                "high": [102.0, 103.0, 104.0],
                                "close": [101.0, 102.0, 103.0],
                                "volume": [1000000, 1200000, 1100000],
                            }
                        ],
                        "adjclose": [{"adjclose": [101.0, 102.0, 103.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def yahoo_data_with_duplicates():
    """Create Yahoo data with duplicate timestamps"""
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
                    "timestamp": [
                        1672531200,
                        1672531200,
                        1672704000,
                    ],  # Duplicate first timestamp
                    "indicators": {
                        "quote": [
                            {
                                "open": [100.0, 101.0, 102.0],
                                "low": [98.0, 99.0, 100.0],
                                "high": [102.0, 103.0, 104.0],
                                "close": [101.0, 102.0, 103.0],
                                "volume": [1000000, 1200000, 1100000],
                            }
                        ],
                        "adjclose": [{"adjclose": [101.0, 102.0, 103.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def symbol_tuples():
    """Create symbol tuples for aggregation"""
    return [
        (DataSource.YAHOO, "AAPL"),
        (DataSource.YAHOO, "MSFT"),
        (DataSource.YAHOO, "GOOGL"),
    ]


@pytest.fixture
def preprocessing_results(valid_preprocessed_symbol):
    """Create preprocessing results list"""
    meta_msft = MetaData(
        symbol="MSFT",
        asset_type=AssetType.EQUITY,
        currency="USD",
        exchange="NASDAQ",
        timezone="America/New_York",
        source=DataSource.YAHOO,
    )
    symbol_msft = PreprocessedSymbol(
        meta=meta_msft, prices=valid_preprocessed_symbol.records
    )

    return [
        valid_preprocessed_symbol,
        symbol_msft,
        ValueError("Processing failed for GOOGL"),
    ]
