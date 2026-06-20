import pytest
from unittest.mock import Mock

from services.preprocessing.validators.preprocessor_validator import (
    PreprocessorValidator,
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
def valid_meta_dict():
    """Create valid meta dictionary"""
    return {
        "symbol": "AAPL",
        "instrumentType": "EQUITY",
        "currency": "USD",
        "exchangeName": "NASDAQ",
        "timezone": "America/New_York",
    }


@pytest.fixture
def valid_records_dict():
    """Create valid records dictionary"""
    return {
        "timestamp": [1672531200, 1672617600, 1672704000],
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


@pytest.fixture
def data_with_none_values():
    """Create data with None values in OHLC"""
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
def data_with_single_record():
    """Create data with a single record"""
    return {
        "chart": {
            "result": [
                {
                    "meta": {
                        "symbol": "MSFT",
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
def data_with_crypto():
    """Create data for a cryptocurrency"""
    return {
        "chart": {
            "result": [
                {
                    "meta": {
                        "symbol": "BTC-USD",
                        "instrumentType": "cryptocurrency",
                        "currency": "USD",
                        "exchangeName": "CRYPTO",
                        "timezone": "UTC",
                    },
                    "timestamp": [1672531200, 1672617600],
                    "indicators": {
                        "quote": [
                            {
                                "open": [10000.0, 10500.0],
                                "low": [9900.0, 10400.0],
                                "high": [10100.0, 10600.0],
                                "close": [10050.0, 10550.0],
                                "volume": [1000, 1200],
                            }
                        ],
                        "adjclose": [{"adjclose": [10050.0, 10550.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def data_with_unsorted_timestamps():
    """Create data with unsorted timestamps"""
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
                    "timestamp": [1672704000, 1672531200, 1672617600],  # Unsorted
                    "indicators": {
                        "quote": [
                            {
                                "open": [102.0, 100.0, 101.0],
                                "low": [100.0, 98.0, 99.0],
                                "high": [104.0, 102.0, 103.0],
                                "close": [103.0, 101.0, 102.0],
                                "volume": [1100000, 1000000, 1200000],
                            }
                        ],
                        "adjclose": [{"adjclose": [103.0, 101.0, 102.0]}],
                    },
                }
            ]
        }
    }


@pytest.fixture
def data_with_duplicate_timestamps():
    """Create data with duplicate timestamps"""
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
                    "timestamp": [1672531200, 1672531200, 1672704000],  # Duplicate
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
