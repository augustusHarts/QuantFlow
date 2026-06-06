# import pytest
# from unittest.mock import (
#     AsyncMock, 
#     Mock
# )
# from pipelines.historical_ingestion.pipeline import (
#     HistoricalIngestion
# )

# # --------------------------------------------------
# # Success
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_run_success(
#     pipeline,
#     provider,
#     processor,
#     transformer
# ):

#     provider.fetch = AsyncMock(
#         side_effect=[
#             {"symbol": "AAPL"},
#             {"symbol": "MSFT"},
#             {"symbol": "GOOG"}
#         ]
#     )

#     processed = Mock(
#         successful={
#             "AAPL": {},
#             "MSFT": {},
#             "GOOG": {}
#         },
#         failed={}
#     )

#     processor.process.return_value = processed

#     transformer.transform.return_value = (
#         "transformed_data"
#     )

#     result = await pipeline.run()

#     assert result == "transformed_data"

# # --------------------------------------------------
# # Provider - All symbols
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_calls_provider_for_each_symbol(
#     pipeline,
#     provider,
#     symbols
# ):

#     provider.fetch = AsyncMock(
#         return_value={}
#     )

#     pipeline.processor.process.return_value = Mock(
#         successful={},
#         failed={}
#     )

#     pipeline.transformer.transform.return_value = {}

#     await pipeline.run()

#     assert provider.fetch.call_count == len(symbols)

# # --------------------------------------------------
# # Processor
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_processor_called(
#     pipeline,
#     provider,
#     processor
# ):

#     provider.fetch = AsyncMock(
#         side_effect=[
#             {"AAPL": 1},
#             {"MSFT": 2},
#             {"GOOG": 3}
#         ]
#     )

#     processor.process.return_value = Mock(
#         successful={},
#         failed={}
#     )

#     pipeline.transformer.transform.return_value = {}

#     await pipeline.run()

#     processor.process.assert_called_once()

# # --------------------------------------------------
# # Transformation
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_transformer_called(
#     pipeline,
#     provider,
#     processor,
#     transformer
# ):

#     provider.fetch = AsyncMock(
#         return_value={}
#     )

#     processed = Mock(
#         successful={},
#         failed={}
#     )

#     processor.process.return_value = processed

#     transformer.transform.return_value = {}

#     await pipeline.run()

#     transformer.transform.assert_called_once_with(
#         processed
#     )

# # --------------------------------------------------
# # 
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_provider_exception_passed_to_processor(
#     pipeline,
#     provider,
#     processor
# ):

#     provider.fetch = AsyncMock(
#         side_effect=[
#             Exception("AAPL failed"),
#             {"MSFT": 1},
#             {"GOOG": 2}
#         ]
#     )

#     processor.process.return_value = Mock(
#         successful={},
#         failed={}
#     )

#     pipeline.transformer.transform.return_value = {}

#     await pipeline.run()

#     args = processor.process.call_args[0]

#     results = args[1]

#     assert isinstance(
#         results[0],
#         Exception
#     )

# # --------------------------------------------------
# # Empty Symbols
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_empty_symbols(
#     logger,
#     provider,
#     processor,
#     transformer
# ):

#     pipeline = HistoricalIngestion(
#         symbols=[],
#         logger=logger,
#         provider=provider,
#         processor=processor,
#         transformer=transformer
#     )

#     processor.process.return_value = Mock(
#         successful={},
#         failed={}
#     )

#     transformer.transform.return_value = {}

#     result = await pipeline.run()

#     assert result == {}

# # --------------------------------------------------
# # Logging
# # --------------------------------------------------
# @pytest.mark.asyncio
# async def test_completion_logged(
#     pipeline,
#     provider,
#     processor,
#     caplog
# ):

#     provider.fetch = AsyncMock(
#         return_value={}
#     )

#     processor.process.return_value = Mock(
#         successful={"AAPL": {}},
#         failed={}
#     )

#     pipeline.transformer.transform.return_value = {}

#     await pipeline.run()

#     assert "Ingestion Completed" in caplog.text