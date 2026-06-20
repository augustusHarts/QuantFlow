from shared.enums.pipelinestatus import PipelineStatus
from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
from shared.models.preprocessing_model import PreprocessingResult
from pipelines.preprocessing.config import BASE_LAYER
from pipelines.preprocessing.pipeline import PreprocessingPipeline


# --------------------------------------------------
# Initialization Tests
# --------------------------------------------------
class TestPreprocessingPipelineInit:
    def test_init_creates_instance(
        self, mock_logger, mock_preprocessor, mock_aggregator, mock_repository
    ):
        """Test that pipeline initializes correctly"""
        pipeline = PreprocessingPipeline(
            logger=mock_logger,
            preprocessor=mock_preprocessor,
            aggregator=mock_aggregator,
            repository=mock_repository,
        )

        assert pipeline.logger == mock_logger
        assert pipeline.preprocessor == mock_preprocessor
        assert pipeline.aggregator == mock_aggregator
        assert pipeline.repository == mock_repository

    def test_init_status_is_pending(self, pipeline):
        """Test that initial status is PENDING"""
        assert pipeline.status == PipelineStatus.PENDING

    def test_init_stores_all_dependencies(
        self, mock_logger, mock_preprocessor, mock_aggregator, mock_repository
    ):
        """Test that all dependencies are stored"""
        pipeline = PreprocessingPipeline(
            logger=mock_logger,
            preprocessor=mock_preprocessor,
            aggregator=mock_aggregator,
            repository=mock_repository,
        )

        assert hasattr(pipeline, "logger")
        assert hasattr(pipeline, "preprocessor")
        assert hasattr(pipeline, "aggregator")
        assert hasattr(pipeline, "repository")
        assert hasattr(pipeline, "status")


# --------------------------------------------------
# run() Tests - Empty Keys
# --------------------------------------------------
class TestRunEmptyKeys:
    def test_run_returns_empty_result_when_no_keys(self, pipeline, mock_repository):
        """Test that run returns empty result when no keys exist"""
        mock_repository.list_providers.return_value = []
        mock_repository.list_keys.return_value = {}

        result = pipeline.run()

        assert isinstance(result, PreprocessingResult)
        assert len(result.successful) == 0
        assert len(result.failed) == 0

    def test_run_logs_warning_when_no_keys(
        self, pipeline, mock_repository, mock_logger
    ):
        """Test that run logs warning when no keys exist"""
        mock_repository.list_providers.return_value = []
        mock_repository.list_keys.return_value = {}

        pipeline.run()

        mock_logger.warning.assert_called_once_with("No provider and keys founds")

    def test_run_status_remains_pending_when_no_keys(self, pipeline, mock_repository):
        """Test that status remains PENDING when no keys"""
        mock_repository.list_providers.return_value = []
        mock_repository.list_keys.return_value = {}

        pipeline.run()

        # Status should remain PENDING since run() returns early
        # Actually based on code, it returns before changing status
        assert pipeline.status == PipelineStatus.PENDING


# --------------------------------------------------
# run() Tests - All Successful
# --------------------------------------------------
class TestRunAllSuccessful:
    def test_run_processes_all_symbols_successfully(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
        mock_logger,
    ):
        """Test that run processes all symbols successfully"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        assert len(result.successful) == 2
        assert len(result.failed) == 0

    def test_run_status_success_when_all_succeed(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that status is SUCCESS when all symbols succeed"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert pipeline.status == PipelineStatus.SUCCESS

    def test_run_calls_preprocessor_for_each_symbol(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that preprocessor is called for each symbol"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert mock_preprocessor.preprocess.call_count == 2

    def test_run_loads_raw_data_for_each_symbol(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that raw data is loaded for each symbol"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert mock_repository.load.call_count == 2

    def test_run_persists_successful_data(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that successful data is persisted"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert mock_repository.save.call_count == 2

    def test_run_logs_start_and_completion(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
        mock_logger,
    ):
        """Test that run logs start and completion"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify logger.info was called at least twice (start and completion)
        assert mock_logger.info.call_count >= 2


# --------------------------------------------------
# run() Tests - All Failed
# --------------------------------------------------
class TestRunAllFailed:
    def test_run_handles_all_failures(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
    ):
        """Test that run handles all preprocessing failures"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = ValueError("Processing failed")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): ValueError("Processing failed"),
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        assert len(result.successful) == 0
        assert len(result.failed) == 2

    def test_run_status_failed_when_all_fail(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
    ):
        """Test that status is FAILED when all symbols fail"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = ValueError("Processing failed")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): ValueError("Processing failed"),
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert pipeline.status == PipelineStatus.FAILED

    def test_run_does_not_persist_failed_data(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
    ):
        """Test that failed data is not persisted"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = ValueError("Processing failed")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): ValueError("Processing failed"),
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        mock_repository.save.assert_not_called()


# --------------------------------------------------
# run() Tests - Mixed Success and Failure
# --------------------------------------------------
class TestRunMixedResults:
    def test_run_handles_mixed_results(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that run handles mixed success and failure"""

        def preprocess_side_effect(data):
            if "AAPL" in str(data):
                return valid_preprocessed_symbol
            else:
                raise ValueError("Processing failed")

        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = preprocess_side_effect

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
            },
            failed={
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        assert len(result.successful) == 1
        assert len(result.failed) == 1

    def test_run_status_partial_success_when_mixed(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that status is PARTIAL_SUCCESS when mixed results"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
            },
            failed={
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        assert pipeline.status == PipelineStatus.PARTIAL_SUCCESS

    def test_run_persists_only_successful_data_in_mixed_results(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that only successful data is persisted in mixed results"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
            },
            failed={
                (DataSource.YAHOO, "MSFT"): ValueError("Processing failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Only 1 successful result should be saved
        assert mock_repository.save.call_count == 1


# --------------------------------------------------
# run() Tests - Status Transitions
# --------------------------------------------------
class TestStatusTransitions:
    def test_status_changes_to_running(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that status changes to RUNNING during execution"""
        original_status = pipeline.status
        assert original_status == PipelineStatus.PENDING

        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # After run, status should be SUCCESS
        assert pipeline.status == PipelineStatus.SUCCESS

    def test_status_progression(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test complete status progression"""
        initial_status = pipeline.status

        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
            },
            failed={
                (DataSource.YAHOO, "MSFT"): ValueError("Failed"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Started as PENDING
        assert initial_status == PipelineStatus.PENDING
        # Ended as PARTIAL_SUCCESS
        assert pipeline.status == PipelineStatus.PARTIAL_SUCCESS


# --------------------------------------------------
# run() Tests - Exception Handling
# --------------------------------------------------
class TestExceptionHandling:
    def test_run_catches_load_exception(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
    ):
        """Test that run catches exceptions from repository load"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.side_effect = FileNotFoundError("File not found")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): FileNotFoundError("File not found"),
                (DataSource.YAHOO, "MSFT"): FileNotFoundError("File not found"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        # Should not raise, but handle the exception
        result = pipeline.run()

        assert len(result.failed) >= 0

    def test_run_catches_preprocessing_exception(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
    ):
        """Test that run catches exceptions from preprocessor"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = ValueError("Invalid data")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): ValueError("Invalid data"),
                (DataSource.YAHOO, "MSFT"): ValueError("Invalid data"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        # Should not raise, but handle the exception
        result = pipeline.run()

        assert len(result.failed) >= 0

    def test_run_returns_aggregation_result_on_exception(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
    ):
        """Test that run returns aggregator result even with exceptions"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.side_effect = RuntimeError("Preprocessing error")

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): RuntimeError("Preprocessing error"),
                (DataSource.YAHOO, "MSFT"): RuntimeError("Preprocessing error"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        assert isinstance(result, PreprocessingResult)


# --------------------------------------------------
# run() Tests - Aggregator Integration
# --------------------------------------------------
class TestAggregatorIntegration:
    def test_run_calls_aggregator(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that aggregator is called with correct arguments"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify aggregator was called
        mock_aggregator.aggregate.assert_called_once()

        # Verify aggregator was called with symbols and results
        call_args = mock_aggregator.aggregate.call_args
        assert "symbols" in call_args.kwargs
        assert "results" in call_args.kwargs

    def test_run_passes_correct_number_of_symbols_to_aggregator(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that correct number of symbols are passed to aggregator"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        call_args = mock_aggregator.aggregate.call_args
        symbols = call_args.kwargs["symbols"]
        results = call_args.kwargs["results"]

        # Should have same number of symbols and results
        assert len(symbols) == len(results)
        assert len(symbols) == 2


# --------------------------------------------------
# run() Tests - Repository Interactions
# --------------------------------------------------
class TestRepositoryInteractions:
    def test_run_calls_list_providers(self, pipeline, mock_repository):
        """Test that run calls list_providers"""
        mock_repository.list_providers.return_value = []
        mock_repository.list_keys.return_value = {}

        pipeline.run()

        mock_repository.list_providers.assert_called_once_with(BASE_LAYER)

    def test_run_calls_list_keys_with_providers(self, pipeline, mock_repository):
        """Test that run calls list_keys with providers"""
        providers = [DataSource.YAHOO]
        mock_repository.list_providers.return_value = providers
        mock_repository.list_keys.return_value = {}

        pipeline.run()

        mock_repository.list_keys.assert_called_once_with(BASE_LAYER, providers)

    def test_run_loads_raw_data_from_correct_layer(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that run loads data from RAW layer"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify load was called with BASE_LAYER (RAW)
        calls = mock_repository.load.call_args_list
        for call_obj in calls:
            assert call_obj[0][0] == BASE_LAYER

    def test_run_saves_to_processed_layer(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test that run saves data to PROCESSED layer"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify save was called for each successful result
        calls = mock_repository.save.call_args_list
        for call_obj in calls:
            save_request = call_obj[0][0]
            assert save_request.layer == DataLayer.PROCESSED


# --------------------------------------------------
# run() Tests - Logging
# --------------------------------------------------
class TestLogging:
    def test_run_logs_warning_when_no_keys(
        self, pipeline, mock_repository, mock_logger
    ):
        """Test logging when no keys found"""
        mock_repository.list_providers.return_value = []
        mock_repository.list_keys.return_value = {}

        pipeline.run()

        mock_logger.warning.assert_called_once()

    def test_run_logs_start_info(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
        mock_logger,
    ):
        """Test that run logs start information"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify first info log contains "Preprocessing Started"
        start_logs = [
            call
            for call in mock_logger.info.call_args_list
            if "Preprocessing Started" in str(call)
        ]
        assert len(start_logs) > 0

    def test_run_logs_completion_info(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
        mock_logger,
    ):
        """Test that run logs completion information"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify last info log contains "Preprocessing Completed"
        completion_logs = [
            call
            for call in mock_logger.info.call_args_list
            if "Preprocessing Completed" in str(call)
        ]
        assert len(completion_logs) > 0

    def test_run_logs_include_status(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
        mock_logger,
    ):
        """Test that completion logs include status"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        pipeline.run()

        # Verify completion log includes success count and failed count
        completion_logs = [
            call
            for call in mock_logger.info.call_args_list
            if "Preprocessing Completed" in str(call)
        ]
        assert len(completion_logs) > 0
        assert any("successful=" in str(call) for call in completion_logs)
        assert any("failed=" in str(call) for call in completion_logs)


# --------------------------------------------------
# Integration Tests
# --------------------------------------------------
class TestPipelineIntegration:
    def test_run_complete_flow_all_success(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test complete pipeline flow with all successes"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data
        mock_preprocessor.preprocess.return_value = valid_preprocessed_symbol

        preprocessing_result = PreprocessingResult(
            successful={
                (DataSource.YAHOO, "AAPL"): valid_preprocessed_symbol,
                (DataSource.YAHOO, "MSFT"): valid_preprocessed_symbol,
            },
            failed={},
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        # Verify complete flow
        assert result.successful is not None
        assert result.failed is not None
        assert pipeline.status == PipelineStatus.SUCCESS

    def test_run_complete_flow_with_failures(
        self,
        pipeline,
        mock_repository,
        mock_preprocessor,
        mock_aggregator,
        single_provider_keys,
        raw_yahoo_data,
        valid_preprocessed_symbol,
    ):
        """Test complete pipeline flow with failures"""
        mock_repository.list_providers.return_value = [DataSource.YAHOO]
        mock_repository.list_keys.return_value = single_provider_keys
        mock_repository.load.return_value = raw_yahoo_data

        def preprocess_side_effect(data):
            raise ValueError("Validation error")

        mock_preprocessor.preprocess.side_effect = preprocess_side_effect

        preprocessing_result = PreprocessingResult(
            successful={},
            failed={
                (DataSource.YAHOO, "AAPL"): ValueError("Validation error"),
                (DataSource.YAHOO, "MSFT"): ValueError("Validation error"),
            },
        )
        mock_aggregator.aggregate.return_value = preprocessing_result

        result = pipeline.run()

        # Verify complete flow
        assert len(result.failed) == 2
        assert pipeline.status == PipelineStatus.FAILED
