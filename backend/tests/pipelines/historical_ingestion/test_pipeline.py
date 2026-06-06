import pytest

from shared.models.ingestion_models import (
    IngestionResult
)

from shared.enums.pipelinestatus import (
    PipelineStatus
)

from pipelines.historical_ingestion.pipeline import (
    HistoricalIngestion
)


# --------------------------------------------------
# Status
# --------------------------------------------------

def test_status_success():

    status = HistoricalIngestion._get_pipeline_status(
        successful_count=2,
        failed_count=0
    )

    assert status == PipelineStatus.SUCCESS


def test_status_failed():

    status = HistoricalIngestion._get_pipeline_status(
        successful_count=0,
        failed_count=2
    )

    assert status == PipelineStatus.FAILED


def test_status_partial_success():

    status = HistoricalIngestion._get_pipeline_status(
        successful_count=1,
        failed_count=1
    )

    assert status == PipelineStatus.PARTIAL_SUCCESS


# --------------------------------------------------
# Persistence
# --------------------------------------------------

def test_persist_raw_data(
    pipeline,
    repository
):

    pipeline._persist_raw_data(
        {
            "AAPL": {"price": 100},
            "MSFT": {"price": 200}
        }
    )

    assert repository.save.call_count == 2


# --------------------------------------------------
# Empty Symbols
# --------------------------------------------------

@pytest.mark.asyncio
async def test_empty_symbols(
    logger,
    provider,
    processor,
    repository
):

    pipeline = HistoricalIngestion(
        symbols=[],
        logger=logger,
        provider=provider,
        processor=processor,
        repository=repository
    )

    result = await pipeline.run()

    assert result == IngestionResult(
        successful={},
        failed={}
    )

    logger.warning.assert_called_once()


# --------------------------------------------------
# Successful Run
# --------------------------------------------------

@pytest.mark.asyncio
async def test_run_success(
    pipeline,
    processor,
    successful_result,
    repository
):

    processor.process.return_value = successful_result

    result = await pipeline.run()

    assert result == successful_result

    assert (
        pipeline.status
        == PipelineStatus.SUCCESS
    )

    processor.process.assert_called_once()

    assert repository.save.call_count == 2


# --------------------------------------------------
# Partial Success
# --------------------------------------------------

@pytest.mark.asyncio
async def test_run_partial_success(
    pipeline,
    processor,
    partial_result
):

    processor.process.return_value = partial_result

    await pipeline.run()

    assert (
        pipeline.status
        == PipelineStatus.PARTIAL_SUCCESS
    )


# --------------------------------------------------
# Failed Run
# --------------------------------------------------

@pytest.mark.asyncio
async def test_run_failed(
    pipeline,
    processor,
    failed_result
):

    processor.process.return_value = failed_result

    await pipeline.run()

    assert (
        pipeline.status
        == PipelineStatus.FAILED
    )


# --------------------------------------------------
# Provider Called For Each Symbol
# --------------------------------------------------

@pytest.mark.asyncio
async def test_provider_called_for_each_symbol(
    pipeline,
    provider,
    processor,
    successful_result
):

    processor.process.return_value = successful_result

    await pipeline.run()

    assert provider.fetch.call_count == 2


# --------------------------------------------------
# Processor Receives Results
# --------------------------------------------------

@pytest.mark.asyncio
async def test_processor_called(
    pipeline,
    processor,
    successful_result
):

    processor.process.return_value = successful_result

    await pipeline.run()

    processor.process.assert_called_once()