import pytest
from datetime import datetime

from shared.models.preprocessing_model import PriceRecord, PreprocessedSymbol, MetaData
from shared.enums.assettype import AssetType
from shared.enums.datasource import DataSource
from backend.services.preprocessing.validators.preprocessor_validator import (
    PreprocessorValidator,
)


@pytest.fixture
def validator():
    return PreprocessorValidator()


@pytest.fixture
def valid_metadata():
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
    return [
        PriceRecord(
            timestamp=datetime(2023, 1, 1),
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        ),
        PriceRecord(
            timestamp=datetime(2023, 1, 2),
            open=101.0,
            low=99.0,
            high=103.0,
            close=102.0,
            adj_close=102.0,
            volume=1200000,
        ),
        PriceRecord(
            timestamp=datetime(2023, 1, 3),
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
    return PreprocessedSymbol(meta=valid_metadata, prices=valid_price_records)


@pytest.fixture
def price_records_with_none_values():
    return [
        PriceRecord(
            timestamp=datetime(2023, 1, 1),
            open=None,
            low=98.0,
            high=102.0,
            close=None,
            adj_close=101.0,
            volume=None,
        ),
        PriceRecord(
            timestamp=datetime(2023, 1, 2),
            open=101.0,
            low=99.0,
            high=103.0,
            close=102.0,
            adj_close=102.0,
            volume=1200000,
        ),
    ]


@pytest.fixture
def price_records_with_duplicates():
    timestamp = datetime(2023, 1, 1)
    return [
        PriceRecord(
            timestamp=timestamp,
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        ),
        PriceRecord(
            timestamp=timestamp,
            open=101.0,
            low=99.0,
            high=103.0,
            close=102.0,
            adj_close=102.0,
            volume=1200000,
        ),
    ]
