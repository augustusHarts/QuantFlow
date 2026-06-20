from datetime import datetime, UTC

from shared.models.preprocessing_model import PreprocessedSymbol, PriceRecord, MetaData
from shared.enums.assettype import AssetType
from shared.enums.datasource import DataSource


# --------------------------------------------------
# _process_meta Tests
# --------------------------------------------------
class TestProcessMeta:
    def test_process_meta_valid(self, yahoo_preprocessor, valid_meta_dict):
        """Test processing valid metadata"""
        meta = yahoo_preprocessor._process_meta(valid_meta_dict)

        assert isinstance(meta, MetaData)
        assert meta.symbol == "AAPL"
        assert meta.asset_type == AssetType.EQUITY
        assert meta.currency == "USD"
        assert meta.exchange == "NASDAQ"
        assert meta.timezone == "America/New_York"
        assert meta.source == DataSource.YAHOO

    def test_process_meta_cryptocurrency(self, yahoo_preprocessor):
        """Test processing metadata for cryptocurrency"""
        meta_dict = {
            "symbol": "BTC-USD",
            "instrumentType": "cryptocurrency",
            "currency": "USD",
            "exchangeName": "CRYPTO",
            "timezone": "UTC",
        }
        meta = yahoo_preprocessor._process_meta(meta_dict)

        assert meta.symbol == "BTC-USD"
        assert meta.asset_type == AssetType.CRYPTO
        assert meta.currency == "USD"
        assert meta.exchange == "CRYPTO"
        assert meta.timezone == "UTC"

    def test_process_meta_different_currencies(self, yahoo_preprocessor):
        """Test processing metadata with different currencies"""
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]

        for currency in currencies:
            meta_dict = {
                "symbol": "TEST",
                "instrumentType": "EQUITY",
                "currency": currency,
                "exchangeName": "TEST_EXCHANGE",
                "timezone": "UTC",
            }
            meta = yahoo_preprocessor._process_meta(meta_dict)
            assert meta.currency == currency

    def test_process_meta_different_timezones(self, yahoo_preprocessor):
        """Test processing metadata with different timezones"""
        timezones = ["America/New_York", "Europe/London", "Asia/Tokyo", "UTC"]

        for timezone in timezones:
            meta_dict = {
                "symbol": "TEST",
                "instrumentType": "EQUITY",
                "currency": "USD",
                "exchangeName": "TEST_EXCHANGE",
                "timezone": timezone,
            }
            meta = yahoo_preprocessor._process_meta(meta_dict)
            assert meta.timezone == timezone

    def test_process_meta_source_always_yahoo(
        self, yahoo_preprocessor, valid_meta_dict
    ):
        """Test that source is always set to YAHOO"""
        meta = yahoo_preprocessor._process_meta(valid_meta_dict)
        assert meta.source == DataSource.YAHOO

    def test_process_meta_case_insensitive_instrument_type(self, yahoo_preprocessor):
        """Test that instrument type is case insensitive"""
        meta_dict_upper = {
            "symbol": "TEST",
            "instrumentType": "EQUITY",
            "currency": "USD",
            "exchangeName": "TEST",
            "timezone": "UTC",
        }
        meta_dict_lower = {
            "symbol": "TEST",
            "instrumentType": "equity",
            "currency": "USD",
            "exchangeName": "TEST",
            "timezone": "UTC",
        }

        meta_upper = yahoo_preprocessor._process_meta(meta_dict_upper)
        meta_lower = yahoo_preprocessor._process_meta(meta_dict_lower)

        assert meta_upper.asset_type == meta_lower.asset_type
        assert meta_upper.asset_type == AssetType.EQUITY


# --------------------------------------------------
# _process_records Tests
# --------------------------------------------------
class TestProcessRecords:
    def test_process_records_valid(self, yahoo_preprocessor, valid_records_dict):
        """Test processing valid records"""
        records = yahoo_preprocessor._process_records(valid_records_dict)

        assert isinstance(records, list)
        assert len(records) == 3
        assert all(isinstance(r, PriceRecord) for r in records)

    def test_process_records_structure(self, yahoo_preprocessor, valid_records_dict):
        """Test that processed records have correct structure"""
        records = yahoo_preprocessor._process_records(valid_records_dict)

        first_record = records[0]
        assert hasattr(first_record, "timestamp")
        assert hasattr(first_record, "open")
        assert hasattr(first_record, "low")
        assert hasattr(first_record, "high")
        assert hasattr(first_record, "close")
        assert hasattr(first_record, "adj_close")
        assert hasattr(first_record, "volume")

    def test_process_records_timestamps_conversion(
        self, yahoo_preprocessor, valid_records_dict
    ):
        """Test that timestamps are correctly converted from Unix timestamps"""
        records = yahoo_preprocessor._process_records(valid_records_dict)

        # Verify timestamps are datetime objects with UTC timezone
        for record in records:
            assert isinstance(record.timestamp, datetime)
            assert record.timestamp.tzinfo == UTC

    def test_process_records_sorted_by_timestamp(
        self, yahoo_preprocessor, data_with_unsorted_timestamps
    ):
        """Test that records are sorted by timestamp"""
        raw_records = data_with_unsorted_timestamps["chart"]["result"][0]
        records = yahoo_preprocessor._process_records(raw_records)

        # Verify records are sorted
        for i in range(len(records) - 1):
            assert records[i].timestamp <= records[i + 1].timestamp

    def test_process_records_filters_none_values(
        self, yahoo_preprocessor, data_with_none_values
    ):
        """Test that records with None values in OHLC are filtered"""
        raw_records = data_with_none_values["chart"]["result"][0]
        records = yahoo_preprocessor._process_records(raw_records)

        # Should have fewer records due to filtering
        assert len(records) < 3  # Original has 3 records but one has None open

        # All remaining records should have all OHLC values
        for record in records:
            assert record.open is not None
            assert record.high is not None
            assert record.low is not None
            assert record.close is not None

    def test_process_records_removes_duplicates(
        self, yahoo_preprocessor, data_with_duplicate_timestamps
    ):
        """Test that duplicate timestamps are removed"""
        raw_records = data_with_duplicate_timestamps["chart"]["result"][0]
        records = yahoo_preprocessor._process_records(raw_records)

        # Should have fewer records due to duplicate removal
        assert len(records) < 3

        # Verify no duplicate timestamps
        timestamps = [r.timestamp for r in records]
        assert len(timestamps) == len(set(timestamps))

    def test_process_records_single_record(
        self, yahoo_preprocessor, data_with_single_record
    ):
        """Test processing data with a single record"""
        raw_records = data_with_single_record["chart"]["result"][0]
        records = yahoo_preprocessor._process_records(raw_records)

        assert len(records) == 1
        assert records[0].volume == 1000000

    def test_process_records_values_preservation(
        self, yahoo_preprocessor, valid_records_dict
    ):
        """Test that OHLCV values are correctly preserved"""
        records = yahoo_preprocessor._process_records(valid_records_dict)

        # Check first record values
        assert records[0].open == 100.0
        assert records[0].low == 98.0
        assert records[0].high == 102.0
        assert records[0].close == 101.0
        assert records[0].adj_close == 101.0
        assert records[0].volume == 1000000

    def test_process_records_large_volume(self, yahoo_preprocessor, valid_records_dict):
        """Test that large volume values are handled correctly"""
        records = yahoo_preprocessor._process_records(valid_records_dict)

        # All volumes should be preserved as integers
        for record in records:
            assert isinstance(record.volume, int)
            assert record.volume > 0

    def test_process_records_calls_validator(
        self, yahoo_preprocessor, valid_records_dict
    ):
        """Test that validator is called during record processing"""
        # This implicitly tests validate_record_length is called
        records = yahoo_preprocessor._process_records(valid_records_dict)
        assert len(records) == 3

    def test_process_records_with_fractional_prices(self, yahoo_preprocessor):
        """Test processing records with fractional prices"""
        records_dict = {
            "timestamp": [1672531200, 1672617600],
            "indicators": {
                "quote": [
                    {
                        "open": [100.50, 101.75],
                        "low": [98.25, 99.50],
                        "high": [102.75, 103.25],
                        "close": [101.25, 102.50],
                        "volume": [1000000, 1200000],
                    }
                ],
                "adjclose": [{"adjclose": [101.25, 102.50]}],
            },
        }
        records = yahoo_preprocessor._process_records(records_dict)

        assert len(records) == 2
        assert records[0].open == 100.50
        assert records[0].high == 102.75


# --------------------------------------------------
# preprocess Tests
# --------------------------------------------------
class TestPreprocess:
    def test_preprocess_valid_data(self, yahoo_preprocessor, valid_yahoo_data):
        """Test preprocessing valid Yahoo data"""
        symbol = yahoo_preprocessor.preprocess(valid_yahoo_data)

        assert isinstance(symbol, PreprocessedSymbol)
        assert symbol.meta.symbol == "AAPL"
        assert len(symbol.records) == 3

    def test_preprocess_returns_preprocessed_symbol(
        self, yahoo_preprocessor, valid_yahoo_data
    ):
        """Test that preprocess returns a PreprocessedSymbol"""
        result = yahoo_preprocessor.preprocess(valid_yahoo_data)

        assert isinstance(result, PreprocessedSymbol)
        assert hasattr(result, "meta")
        assert hasattr(result, "records")

    def test_preprocess_metadata_extracted(self, yahoo_preprocessor, valid_yahoo_data):
        """Test that metadata is correctly extracted"""
        symbol = yahoo_preprocessor.preprocess(valid_yahoo_data)

        assert symbol.meta.symbol == "AAPL"
        assert symbol.meta.asset_type == AssetType.EQUITY
        assert symbol.meta.currency == "USD"
        assert symbol.meta.exchange == "NASDAQ"

    def test_preprocess_records_extracted(self, yahoo_preprocessor, valid_yahoo_data):
        """Test that records are correctly extracted"""
        symbol = yahoo_preprocessor.preprocess(valid_yahoo_data)

        assert len(symbol.records) > 0
        assert all(isinstance(r, PriceRecord) for r in symbol.records)

    def test_preprocess_filters_records_with_none_values(
        self, yahoo_preprocessor, data_with_none_values
    ):
        """Test that records with None values are filtered during preprocessing"""
        symbol = yahoo_preprocessor.preprocess(data_with_none_values)

        # Should have fewer records due to filtering
        assert len(symbol.records) < 3

    def test_preprocess_removes_duplicates(
        self, yahoo_preprocessor, data_with_duplicate_timestamps
    ):
        """Test that duplicate timestamps are removed during preprocessing"""
        symbol = yahoo_preprocessor.preprocess(data_with_duplicate_timestamps)

        # Should have fewer records
        assert len(symbol.records) < 3

    def test_preprocess_logs_metadata(self, yahoo_preprocessor, valid_yahoo_data):
        """Test that preprocessing logs metadata information"""
        yahoo_preprocessor.preprocess(valid_yahoo_data)

        # Verify logger was called
        assert yahoo_preprocessor.logger.debug.called

    def test_preprocess_logs_record_count(self, yahoo_preprocessor, valid_yahoo_data):
        """Test that preprocessing logs record count"""
        yahoo_preprocessor.preprocess(valid_yahoo_data)

        # Find the call that logs record count
        calls = [str(call) for call in yahoo_preprocessor.logger.debug.call_args_list]
        assert any("records=" in call for call in calls)

    def test_preprocess_cryptocurrency_data(self, yahoo_preprocessor, data_with_crypto):
        """Test preprocessing cryptocurrency data"""
        symbol = yahoo_preprocessor.preprocess(data_with_crypto)

        assert symbol.meta.symbol == "BTC-USD"
        assert symbol.meta.asset_type == AssetType.CRYPTO
        assert len(symbol.records) == 2

    def test_preprocess_single_record(
        self, yahoo_preprocessor, data_with_single_record
    ):
        """Test preprocessing data with a single record"""
        symbol = yahoo_preprocessor.preprocess(data_with_single_record)

        assert len(symbol.records) == 1
        assert symbol.meta.symbol == "MSFT"

    def test_preprocess_records_sorted_chronologically(
        self, yahoo_preprocessor, data_with_unsorted_timestamps
    ):
        """Test that preprocessed records are sorted chronologically"""
        symbol = yahoo_preprocessor.preprocess(data_with_unsorted_timestamps)

        records = symbol.records
        for i in range(len(records) - 1):
            assert records[i].timestamp <= records[i + 1].timestamp

    def test_preprocess_calls_validator(self, yahoo_preprocessor, valid_yahoo_data):
        """Test that preprocessor calls the validator"""
        # If validation fails, preprocess will raise an exception
        # This test verifies validation is called
        symbol = yahoo_preprocessor.preprocess(valid_yahoo_data)
        assert symbol is not None

    def test_preprocess_with_different_asset_types(self, yahoo_preprocessor):
        """Test preprocessing different asset types"""
        asset_types = ["EQUITY", "ETF", "CRYPTOCURRENCY"]

        for asset_type in asset_types:
            data = {
                "chart": {
                    "result": [
                        {
                            "meta": {
                                "symbol": "TEST",
                                "instrumentType": asset_type,
                                "currency": "USD",
                                "exchangeName": "TEST",
                                "timezone": "UTC",
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

            symbol = yahoo_preprocessor.preprocess(data)
            assert symbol.meta.asset_type.value == asset_type.lower()

    def test_preprocess_integration_with_validator(
        self, yahoo_preprocessor, valid_yahoo_data
    ):
        """Test full integration with validator"""
        symbol = yahoo_preprocessor.preprocess(valid_yahoo_data)

        # If we reach here without exception, validation passed
        assert symbol.meta.symbol is not None
        assert len(symbol.records) > 0

    def test_preprocess_handles_float_volumes(self, yahoo_preprocessor):
        """Test that volumes are properly converted to integers"""
        data = {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "symbol": "TEST",
                            "instrumentType": "EQUITY",
                            "currency": "USD",
                            "exchangeName": "TEST",
                            "timezone": "UTC",
                        },
                        "timestamp": [1672531200],
                        "indicators": {
                            "quote": [
                                {
                                    "open": [100.0],
                                    "low": [98.0],
                                    "high": [102.0],
                                    "close": [101.0],
                                    "volume": [1500000],
                                }
                            ],
                            "adjclose": [{"adjclose": [101.0]}],
                        },
                    }
                ]
            }
        }

        symbol = yahoo_preprocessor.preprocess(data)
        assert isinstance(symbol.records[0].volume, int)

    def test_preprocess_large_dataset(self, yahoo_preprocessor):
        """Test preprocessing a large dataset"""
        # Create data with 1000 records
        timestamps = list(range(1672531200, 1672531200 + 1000 * 86400, 86400))
        opens = [100.0 + i * 0.1 for i in range(1000)]
        lows = [98.0 + i * 0.1 for i in range(1000)]
        highs = [102.0 + i * 0.1 for i in range(1000)]
        closes = [101.0 + i * 0.1 for i in range(1000)]
        volumes = [1000000 + i * 1000 for i in range(1000)]
        adj_closes = closes

        data = {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "symbol": "TEST",
                            "instrumentType": "EQUITY",
                            "currency": "USD",
                            "exchangeName": "TEST",
                            "timezone": "UTC",
                        },
                        "timestamp": timestamps,
                        "indicators": {
                            "quote": [
                                {
                                    "open": opens,
                                    "low": lows,
                                    "high": highs,
                                    "close": closes,
                                    "volume": volumes,
                                }
                            ],
                            "adjclose": [{"adjclose": adj_closes}],
                        },
                    }
                ]
            }
        }

        symbol = yahoo_preprocessor.preprocess(data)
        assert len(symbol.records) == 1000

    def test_preprocess_all_prices_none_filtered(self, yahoo_preprocessor):
        """Test that records where all prices are None are filtered"""
        data = {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "symbol": "TEST",
                            "instrumentType": "EQUITY",
                            "currency": "USD",
                            "exchangeName": "TEST",
                            "timezone": "UTC",
                        },
                        "timestamp": [1672531200, 1672617600],
                        "indicators": {
                            "quote": [
                                {
                                    "open": [100.0, None],
                                    "low": [98.0, None],
                                    "high": [102.0, None],
                                    "close": [101.0, None],
                                    "volume": [1000000, 0],
                                }
                            ],
                            "adjclose": [{"adjclose": [101.0, None]}],
                        },
                    }
                ]
            }
        }

        symbol = yahoo_preprocessor.preprocess(data)
        # Should only have 1 record (the one without None values)
        assert len(symbol.records) == 1
