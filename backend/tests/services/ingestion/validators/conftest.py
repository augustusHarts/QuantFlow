import pytest

from services.ingestion.validators.yahoo_validator import YahooValidator


@pytest.fixture
def validator():
    return YahooValidator()


@pytest.fixture
def valid_payload():
    return {
        "chart": {
            "result": [
                {
                    "timestamp": [1, 2, 3],
                    "indicators": {
                        "quote": [
                            {
                                "open": [1.0, 2.0, 3.0],
                                "high": [2.0, 3.0, 4.0],
                                "low": [0.5, 1.5, 2.5],
                                "close": [1.5, 2.5, 3.5],
                                "volume": [100, 200, 300],
                            }
                        ],
                        "adjclose": [{"adjclose": [1.5, 2.5, 3.5]}],
                    },
                }
            ],
            "error": None,
        }
    }
