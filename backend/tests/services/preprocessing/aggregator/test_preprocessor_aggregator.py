from copy import deepcopy

from shared.models.preprocessing_model import PreprocessingResult, PreprocessedSymbol
from shared.enums.datasource import DataSource


# --------------------------------------------------
# PreprocessorAggregator.aggregate() Tests
# --------------------------------------------------
class TestAggregatorAggregate:
    def test_aggregate_all_successful(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test aggregation when all symbols process successfully"""
        meta_msft = deepcopy(valid_preprocessed_symbol.meta)
        meta_msft.symbol = "MSFT"
        symbol_msft = PreprocessedSymbol(
            meta=meta_msft, records=valid_preprocessed_symbol.records
        )

        meta_googl = deepcopy(valid_preprocessed_symbol.meta)
        meta_googl.symbol = "GOOGL"
        symbol_googl = PreprocessedSymbol(
            meta=meta_googl, records=valid_preprocessed_symbol.records
        )

        results = [valid_preprocessed_symbol, symbol_msft, symbol_googl]

        result = aggregator.aggregate(symbol_tuples, results)

        assert isinstance(result, PreprocessingResult)
        assert len(result.successful) == 3
        assert len(result.failed) == 0
        assert (DataSource.YAHOO, "AAPL") in result.successful
        assert (DataSource.YAHOO, "MSFT") in result.successful
        assert (DataSource.YAHOO, "GOOGL") in result.successful

    def test_aggregate_all_failed(self, aggregator, symbol_tuples):
        """Test aggregation when all symbols fail"""
        errors = [
            ValueError("AAPL processing failed"),
            ValueError("MSFT processing failed"),
            ValueError("GOOGL processing failed"),
        ]

        result = aggregator.aggregate(symbol_tuples, errors)

        assert isinstance(result, PreprocessingResult)
        assert len(result.successful) == 0
        assert len(result.failed) == 3
        assert (DataSource.YAHOO, "AAPL") in result.failed
        assert (DataSource.YAHOO, "MSFT") in result.failed
        assert (DataSource.YAHOO, "GOOGL") in result.failed

    def test_aggregate_mixed_success_and_failure(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test aggregation with mixed successful and failed results"""
        meta_msft = deepcopy(valid_preprocessed_symbol.meta)
        meta_msft.symbol = "MSFT"
        symbol_msft = PreprocessedSymbol(
            meta=meta_msft, records=valid_preprocessed_symbol.records
        )

        error = ValueError("GOOGL processing failed")
        results = [valid_preprocessed_symbol, symbol_msft, error]

        result = aggregator.aggregate(symbol_tuples, results)

        assert len(result.successful) == 2
        assert len(result.failed) == 1
        assert (DataSource.YAHOO, "AAPL") in result.successful
        assert (DataSource.YAHOO, "MSFT") in result.successful
        assert (DataSource.YAHOO, "GOOGL") in result.failed
        assert isinstance(result.failed[(DataSource.YAHOO, "GOOGL")], ValueError)

    def test_aggregate_different_error_types(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test aggregation with different types of exceptions"""
        value_error = ValueError("Value error")
        runtime_error = RuntimeError("Runtime error")
        type_error = TypeError("Type error")
        results = [value_error, runtime_error, type_error]

        result = aggregator.aggregate(symbol_tuples, results)

        assert len(result.successful) == 0
        assert len(result.failed) == 3
        assert isinstance(result.failed[(DataSource.YAHOO, "AAPL")], ValueError)
        assert isinstance(result.failed[(DataSource.YAHOO, "MSFT")], RuntimeError)
        assert isinstance(result.failed[(DataSource.YAHOO, "GOOGL")], TypeError)

    def test_aggregate_single_symbol(self, aggregator, valid_preprocessed_symbol):
        """Test aggregation with a single symbol"""
        symbols = [(DataSource.YAHOO, "AAPL")]
        results = [valid_preprocessed_symbol]

        result = aggregator.aggregate(symbols, results)

        assert len(result.successful) == 1
        assert len(result.failed) == 0
        assert (DataSource.YAHOO, "AAPL") in result.successful

    def test_aggregate_empty_lists(self, aggregator):
        """Test aggregation with empty symbol and results lists"""
        symbols = []
        results = []

        result = aggregator.aggregate(symbols, results)

        assert len(result.successful) == 0
        assert len(result.failed) == 0

    def test_aggregate_preserves_preprocessed_symbol(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test that aggregation preserves the PreprocessedSymbol content"""
        results = [valid_preprocessed_symbol] + [ValueError("error")] * 2

        result = aggregator.aggregate(symbol_tuples, results)

        stored_symbol = result.successful[(DataSource.YAHOO, "AAPL")]
        assert stored_symbol.meta.symbol == valid_preprocessed_symbol.meta.symbol
        assert len(stored_symbol.records) == len(valid_preprocessed_symbol.records)

    def test_aggregate_preserves_error_message(self, aggregator, symbol_tuples):
        """Test that aggregation preserves error messages"""
        error_msg = "Custom error message with details"
        error = ValueError(error_msg)
        results = [error] * 3

        result = aggregator.aggregate(symbol_tuples, results)

        stored_error = result.failed[(DataSource.YAHOO, "AAPL")]
        assert str(stored_error) == error_msg

    def test_aggregate_logs_errors(self, aggregator, symbol_tuples):
        """Test that aggregation logs errors"""
        error = ValueError("Test error message")
        results = [error] * 3

        aggregator.aggregate(symbol_tuples, results)

        # Verify logger was called for errors
        assert aggregator.logger.error.call_count == 3

        # Verify error details are logged
        call_args = aggregator.logger.error.call_args_list[0]
        assert "AAPL" in call_args[0]
        assert "ValueError" in call_args[0]

    def test_aggregate_with_different_symbols_multiple_providers(
        self, aggregator, valid_preprocessed_symbol
    ):
        """Test aggregation with same provider but different symbols"""
        meta_msft = deepcopy(valid_preprocessed_symbol.meta)
        meta_msft.symbol = "MSFT"
        symbol_msft = PreprocessedSymbol(
            meta=meta_msft, records=valid_preprocessed_symbol.records
        )

        symbols = [(DataSource.YAHOO, "AAPL"), (DataSource.YAHOO, "MSFT")]
        results = [valid_preprocessed_symbol, symbol_msft]

        result = aggregator.aggregate(symbols, results)

        assert len(result.successful) == 2
        assert (DataSource.YAHOO, "AAPL") in result.successful
        assert (DataSource.YAHOO, "MSFT") in result.successful

    def test_aggregate_result_structure(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test that aggregation result has correct structure"""
        results = [valid_preprocessed_symbol] + [ValueError("error")] * 2

        result = aggregator.aggregate(symbol_tuples, results)

        assert hasattr(result, "successful")
        assert hasattr(result, "failed")
        assert isinstance(result.successful, dict)
        assert isinstance(result.failed, dict)

    def test_aggregate_logs_successful_symbols(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test that aggregation doesn't log successful symbols"""
        meta_msft = deepcopy(valid_preprocessed_symbol.meta)
        meta_msft.symbol = "MSFT"
        symbol_msft = PreprocessedSymbol(
            meta=meta_msft, records=valid_preprocessed_symbol.records
        )
        results = [valid_preprocessed_symbol, symbol_msft, ValueError("error")]

        aggregator.aggregate(symbol_tuples, results)

        # Only one error should be logged
        assert aggregator.logger.error.call_count == 1

    def test_aggregate_large_number_of_symbols(self, aggregator):
        """Test aggregation with a large number of symbols"""
        num_symbols = 100
        symbols = [(DataSource.YAHOO, f"SYM{i}") for i in range(num_symbols)]
        results = [ValueError(f"Error {i}") for i in range(num_symbols)]

        result = aggregator.aggregate(symbols, results)

        assert len(result.successful) == 0
        assert len(result.failed) == num_symbols

    def test_aggregate_with_special_characters_in_symbol(self, aggregator):
        """Test aggregation with special characters in symbol names"""
        symbols = [
            (DataSource.YAHOO, "BRK.B"),
            (DataSource.YAHOO, "BRK-A"),
            (DataSource.YAHOO, "BF/A"),
        ]
        results = [ValueError("error")] * 3

        result = aggregator.aggregate(symbols, results)

        assert (DataSource.YAHOO, "BRK.B") in result.failed
        assert (DataSource.YAHOO, "BRK-A") in result.failed
        assert (DataSource.YAHOO, "BF/A") in result.failed

    def test_aggregate_maintains_order(
        self, aggregator, symbol_tuples, valid_preprocessed_symbol
    ):
        """Test that aggregation maintains symbol order in results"""
        meta_msft = deepcopy(valid_preprocessed_symbol.meta)
        meta_msft.symbol = "MSFT"
        symbol_msft = PreprocessedSymbol(
            meta=meta_msft, records=valid_preprocessed_symbol.records
        )
        meta_googl = deepcopy(valid_preprocessed_symbol.meta)
        meta_googl.symbol = "GOOGL"
        symbol_googl = PreprocessedSymbol(
            meta=meta_googl, records=valid_preprocessed_symbol.records
        )
        results = [valid_preprocessed_symbol, symbol_msft, symbol_googl]

        result = aggregator.aggregate(symbol_tuples, results)

        # All symbols should be present
        assert len(result.successful) == 3
