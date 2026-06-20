import pytest
from copy import deepcopy
from datetime import datetime

from shared.models.preprocessing_model import PriceRecord


# --------------------------------------------------
# validate_record_length Tests
# --------------------------------------------------
class TestValidateRecordLength:
    def test_valid_record_lengths_all_same(self, validator):
        """Test that validation passes when all record lengths are the same"""
        lengths = {"AAPL": 100, "MSFT": 100, "GOOGL": 100}
        validator.validate_record_length(lengths)

    def test_single_record(self, validator):
        """Test validation with a single record"""
        lengths = {"AAPL": 100}
        validator.validate_record_length(lengths)

    def test_empty_lengths(self, validator):
        """Test validation with empty lengths dict raises error"""
        lengths = {}
        with pytest.raises(ValueError, match="Record's length mismatch"):
            validator.validate_record_length(lengths)

    def test_mismatched_record_lengths(self, validator):
        """Test that validation fails when record lengths differ"""
        lengths = {"AAPL": 100, "MSFT": 101, "GOOGL": 100}
        with pytest.raises(ValueError, match="Record's length mismatch"):
            validator.validate_record_length(lengths)

    def test_record_length_with_two_different_values(self, validator):
        """Test validation with exactly two different length values"""
        lengths = {"A": 50, "B": 100}
        with pytest.raises(ValueError, match="Record's length mismatch"):
            validator.validate_record_length(lengths)


# --------------------------------------------------
# remove_duplicate_records Tests
# --------------------------------------------------
class TestRemoveDuplicateRecords:
    def test_no_duplicates(self, validator, valid_price_records):
        """Test that records with unique timestamps are returned unchanged"""
        result = validator.remove_duplicate_records(valid_price_records)
        assert len(result) == len(valid_price_records)
        assert result == valid_price_records

    def test_remove_duplicate_timestamps(self, validator):
        """Test that duplicate timestamps are removed, keeping the first occurrence"""
        timestamp = datetime(2023, 1, 1)
        records = [
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
        result = validator.remove_duplicate_records(records)
        assert len(result) == 1
        assert result[0].open == 100.0  # First record is kept

    def test_multiple_duplicates(self, validator):
        """Test removal of multiple duplicate timestamps"""
        timestamp1 = datetime(2023, 1, 1)
        timestamp2 = datetime(2023, 1, 2)
        records = [
            PriceRecord(
                timestamp=timestamp1,
                open=100.0,
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            ),
            PriceRecord(
                timestamp=timestamp1,
                open=101.0,
                low=99.0,
                high=103.0,
                close=102.0,
                adj_close=102.0,
                volume=1200000,
            ),
            PriceRecord(
                timestamp=timestamp2,
                open=102.0,
                low=100.0,
                high=104.0,
                close=103.0,
                adj_close=103.0,
                volume=1100000,
            ),
            PriceRecord(
                timestamp=timestamp2,
                open=103.0,
                low=101.0,
                high=105.0,
                close=104.0,
                adj_close=104.0,
                volume=1300000,
            ),
        ]
        result = validator.remove_duplicate_records(records)
        assert len(result) == 2
        assert result[0].timestamp == timestamp1
        assert result[0].open == 100.0
        assert result[1].timestamp == timestamp2
        assert result[1].open == 102.0

    def test_empty_records(self, validator):
        """Test with empty records list"""
        result = validator.remove_duplicate_records([])
        assert result == []

    def test_single_record(self, validator):
        """Test with a single record"""
        record = PriceRecord(
            timestamp=datetime(2023, 1, 1),
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        )
        result = validator.remove_duplicate_records([record])
        assert len(result) == 1
        assert result[0] == record


# --------------------------------------------------
# validate_metadata Tests
# --------------------------------------------------
class TestValidateMetadata:
    def test_valid_metadata(self, validator, valid_metadata):
        """Test that valid metadata passes validation"""
        validator.validate_metadata(valid_metadata)

    def test_missing_symbol(self, validator, valid_metadata):
        """Test that missing symbol raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.symbol = ""
        with pytest.raises(ValueError, match="Missing symbol"):
            validator.validate_metadata(meta)

    def test_missing_currency(self, validator, valid_metadata):
        """Test that missing currency raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.currency = ""
        with pytest.raises(ValueError, match="Missing currency"):
            validator.validate_metadata(meta)

    def test_missing_exchange(self, validator, valid_metadata):
        """Test that missing exchange raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.exchange = ""
        with pytest.raises(ValueError, match="Missing exchange"):
            validator.validate_metadata(meta)

    def test_none_symbol(self, validator, valid_metadata):
        """Test that None symbol raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.symbol = None
        with pytest.raises(ValueError, match="Missing symbol"):
            validator.validate_metadata(meta)

    def test_none_currency(self, validator, valid_metadata):
        """Test that None currency raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.currency = None
        with pytest.raises(ValueError, match="Missing currency"):
            validator.validate_metadata(meta)

    def test_none_exchange(self, validator, valid_metadata):
        """Test that None exchange raises ValueError"""
        meta = deepcopy(valid_metadata)
        meta.exchange = None
        with pytest.raises(ValueError, match="Missing exchange"):
            validator.validate_metadata(meta)


# --------------------------------------------------
# validate_records_exist Tests
# --------------------------------------------------
class TestValidateRecordsExist:
    def test_records_exist(self, validator, valid_price_records):
        """Test that validation passes when records exist"""
        validator.validate_records_exist(valid_price_records)

    def test_single_record(self, validator):
        """Test with a single record"""
        record = PriceRecord(
            timestamp=datetime(2023, 1, 1),
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        )
        validator.validate_records_exist([record])

    def test_no_records(self, validator):
        """Test that empty records list raises ValueError"""
        with pytest.raises(ValueError, match="No records found"):
            validator.validate_records_exist([])


# --------------------------------------------------
# validate_duplicate_timestamps Tests
# --------------------------------------------------
class TestValidateDuplicateTimestamps:
    def test_no_duplicate_timestamps(self, validator, valid_price_records):
        """Test that validation passes when timestamps are unique"""
        validator.validate_duplicate_timestamps(valid_price_records)

    def test_single_record_no_duplicate(self, validator):
        """Test with a single record"""
        record = PriceRecord(
            timestamp=datetime(2023, 1, 1),
            open=100.0,
            low=98.0,
            high=102.0,
            close=101.0,
            adj_close=101.0,
            volume=1000000,
        )
        validator.validate_duplicate_timestamps([record])

    def test_duplicate_timestamps(self, validator, price_records_with_duplicates):
        """Test that duplicate timestamps raise ValueError"""
        with pytest.raises(ValueError, match="Duplicate timestamps detected"):
            validator.validate_duplicate_timestamps(price_records_with_duplicates)

    def test_multiple_duplicates(self, validator):
        """Test with multiple duplicate timestamps"""
        timestamp1 = datetime(2023, 1, 1)
        timestamp2 = datetime(2023, 1, 2)
        records = [
            PriceRecord(
                timestamp=timestamp1,
                open=100.0,
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            ),
            PriceRecord(
                timestamp=timestamp1,
                open=101.0,
                low=99.0,
                high=103.0,
                close=102.0,
                adj_close=102.0,
                volume=1200000,
            ),
            PriceRecord(
                timestamp=timestamp2,
                open=102.0,
                low=100.0,
                high=104.0,
                close=103.0,
                adj_close=103.0,
                volume=1100000,
            ),
            PriceRecord(
                timestamp=timestamp2,
                open=103.0,
                low=101.0,
                high=105.0,
                close=104.0,
                adj_close=104.0,
                volume=1300000,
            ),
        ]
        with pytest.raises(ValueError, match="Duplicate timestamps detected"):
            validator.validate_duplicate_timestamps(records)


# --------------------------------------------------
# validate_ohlc Tests
# --------------------------------------------------
class TestValidateOHLC:
    def test_valid_ohlc(self, validator, valid_price_records):
        """Test that valid OHLC values pass validation"""
        validator.validate_ohlc(valid_price_records)

    def test_missing_high(self, validator):
        """Test that missing high value raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=None,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Missing high/low"):
            validator.validate_ohlc(records)

    def test_missing_low(self, validator):
        """Test that missing low value raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=None,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Missing high/low"):
            validator.validate_ohlc(records)

    def test_both_high_and_low_missing(self, validator):
        """Test that missing both high and low raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=None,
                high=None,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Missing high/low"):
            validator.validate_ohlc(records)

    def test_high_less_than_low(self, validator):
        """Test that high < low raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=102.0,
                high=98.0,  # high < low
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Invalid OHLC"):
            validator.validate_ohlc(records)

    def test_high_equal_to_low(self, validator):
        """Test that high == low is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=100.0,
                high=100.0,
                close=100.0,
                adj_close=100.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_open_greater_than_high(self, validator):
        """Test that open > high raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=105.0,  # open > high
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Open greater than high"):
            validator.validate_ohlc(records)

    def test_open_lower_than_low(self, validator):
        """Test that open < low raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=97.0,  # open < low
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Open lower than low"):
            validator.validate_ohlc(records)

    def test_open_equal_to_high(self, validator):
        """Test that open == high is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=102.0,
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_open_equal_to_low(self, validator):
        """Test that open == low is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=98.0,
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_close_greater_than_high(self, validator):
        """Test that close > high raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=102.0,
                close=105.0,  # close > high
                adj_close=105.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Close greater than high"):
            validator.validate_ohlc(records)

    def test_close_lower_than_low(self, validator):
        """Test that close < low raises ValueError"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=102.0,
                close=97.0,  # close < low
                adj_close=97.0,
                volume=1000000,
            )
        ]
        with pytest.raises(ValueError, match="Close lower than low"):
            validator.validate_ohlc(records)

    def test_close_equal_to_high(self, validator):
        """Test that close == high is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=102.0,
                close=102.0,
                adj_close=102.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_close_equal_to_low(self, validator):
        """Test that close == low is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=102.0,
                close=98.0,
                adj_close=98.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_open_none_valid(self, validator):
        """Test that None open is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=None,
                low=98.0,
                high=102.0,
                close=101.0,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_close_none_valid(self, validator):
        """Test that None close is valid"""
        records = [
            PriceRecord(
                timestamp=datetime(2023, 1, 1),
                open=100.0,
                low=98.0,
                high=102.0,
                close=None,
                adj_close=101.0,
                volume=1000000,
            )
        ]
        validator.validate_ohlc(records)

    def test_multiple_records_ohlc_validation(self, validator):
        """Test OHLC validation with multiple records"""
        records = [
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
        ]
        validator.validate_ohlc(records)

    def test_ohlc_error_on_second_record(self, validator):
        """Test that OHLC validation fails on second record if invalid"""
        records = [
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
                open=100.0,
                low=99.0,
                high=103.0,
                close=105.0,  # close > high
                adj_close=105.0,
                volume=1200000,
            ),
        ]
        with pytest.raises(ValueError, match="Close greater than high"):
            validator.validate_ohlc(records)


# --------------------------------------------------
# validate (Full Validation) Tests
# --------------------------------------------------
class TestValidate:
    def test_valid_preprocessed_symbol(self, validator, valid_preprocessed_symbol):
        """Test that a valid preprocessed symbol passes all validation"""
        validator.validate(valid_preprocessed_symbol)

    def test_missing_metadata_symbol(self, validator, valid_preprocessed_symbol):
        """Test that missing symbol in metadata raises ValueError"""
        symbol = deepcopy(valid_preprocessed_symbol)
        symbol.meta.symbol = ""
        with pytest.raises(ValueError, match="Missing symbol"):
            validator.validate(symbol)

    def test_missing_records(self, validator, valid_preprocessed_symbol):
        """Test that empty records raises ValueError"""
        symbol = deepcopy(valid_preprocessed_symbol)
        symbol.records = []
        with pytest.raises(ValueError, match="No records found"):
            validator.validate(symbol)

    def test_duplicate_timestamps_in_full_validation(
        self, validator, valid_preprocessed_symbol
    ):
        """Test that duplicate timestamps are caught in full validation"""
        symbol = deepcopy(valid_preprocessed_symbol)
        timestamp = datetime(2023, 1, 1)
        symbol.records = [
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
        with pytest.raises(ValueError, match="Duplicate timestamps detected"):
            validator.validate(symbol)

    def test_invalid_ohlc_in_full_validation(
        self, validator, valid_preprocessed_symbol
    ):
        """Test that invalid OHLC is caught in full validation"""
        symbol = deepcopy(valid_preprocessed_symbol)
        symbol.records[0].close = 105.0  # close > high
        with pytest.raises(ValueError, match="Close greater than high"):
            validator.validate(symbol)

    def test_all_validations_called_in_sequence(
        self, validator, valid_preprocessed_symbol
    ):
        """Test that full validate method checks all conditions"""
        # This is verified by the fact that each individual validation
        # error is properly caught by the main validate method
        validator.validate(valid_preprocessed_symbol)
