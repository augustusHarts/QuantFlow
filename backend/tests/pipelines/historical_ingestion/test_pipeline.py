import pytest

from shared.models.ingestion_models import Result

from shared.enums.pipelinestatus import PipelineStatus

from pipelines.ingestions.historical.pipeline import HistoricalIngestion

from pipelines.ingestions.historical.tasks import get_pipeline_status


# --------------------------------------------------
# Status
# --------------------------------------------------


def test_status_success():

    status = get_pipeline_status(successful_count=2, failed_count=0)

    assert status == PipelineStatus.SUCCESS


def test_status_failed():

    status = get_pipeline_status(successful_count=0, failed_count=2)

    assert status == PipelineStatus.FAILED


def test_status_partial_success():

    status = get_pipeline_status(successful_count=1, failed_count=1)

    assert status == PipelineStatus.PARTIAL_SUCCESS


# --------------------------------------------------
# Persistence
# --------------------------------------------------


def test_persist_raw_data(provider, repository):

    from backend.pipelines.ingestions.historical.tasks import persist_raw_data

    persist_raw_data(
        repository, provider, {"AAPL": {"price": 100}, "MSFT": {"price": 200}}
    )

    assert repository.save.call_count == 2


# --------------------------------------------------
# Empty Symbols
# --------------------------------------------------


@pytest.mark.asyncio
async def test_empty_symbols(logger, provider, aggregator, repository):

    pipeline = HistoricalIngestion(
        symbols=[],
        logger=logger,
        provider=provider,
        aggregator=aggregator,
        repository=repository,
    )

    result = await pipeline.run()

    assert result == Result(successful={}, failed={})

    logger.warning.assert_called_once()


# --------------------------------------------------
# Successful Run
# --------------------------------------------------


@pytest.mark.asyncio
async def test_run_success(pipeline, aggregator, successful_result, repository):

    aggregator.aggregate.return_value = successful_result

    result = await pipeline.run()

    assert result == successful_result

    assert pipeline.status == PipelineStatus.SUCCESS

    aggregator.aggregate.assert_called_once()

    assert repository.save.call_count == 2


# --------------------------------------------------
# Partial Success
# --------------------------------------------------


@pytest.mark.asyncio
async def test_run_partial_success(pipeline, aggregator, partial_result):

    aggregator.aggregate.return_value = partial_result

    await pipeline.run()

    assert pipeline.status == PipelineStatus.PARTIAL_SUCCESS


# --------------------------------------------------
# Failed Run
# --------------------------------------------------


@pytest.mark.asyncio
async def test_run_failed(pipeline, aggregator, failed_result):

    aggregator.aggregate.return_value = failed_result

    await pipeline.run()

    assert pipeline.status == PipelineStatus.FAILED


# --------------------------------------------------
# Provider Called For Each Symbol
# --------------------------------------------------


@pytest.mark.asyncio
async def test_provider_called_for_each_symbol(
    pipeline, provider, aggregator, successful_result
):

    aggregator.aggregate.return_value = successful_result

    await pipeline.run()

    assert provider.fetch.call_count == 2


# --------------------------------------------------
# aggregator Receives Results
# --------------------------------------------------


@pytest.mark.asyncio
async def test_aggregator_called(pipeline, aggregator, successful_result):

    aggregator.aggregate.return_value = successful_result

    await pipeline.run()

    aggregator.aggregate.assert_called_once()
