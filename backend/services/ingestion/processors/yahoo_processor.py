from typing import Any

from shared.decorators.logging import log_stage
from shared.models.ingestion_models import IngestionResult
from services.ingestion.interfaces.processor import Processor
from shared.models.ingestion_models import MarketSymbol

class YahooProcessor(Processor):

    def __init__(self, logger):
        self.logger = logger

    @log_stage("Processing Results")
    def process(
        self,
        symbols: list[MarketSymbol],
        results: list[dict[str, Any] | BaseException]
    ) -> IngestionResult:

        successful: dict[str, dict[str, Any]] = {}
        failed: dict[str, BaseException] = {}

        for symbol, result in zip(symbols, results):

            if isinstance(result, BaseException):

                failed[symbol.ticker] = result

                self.logger.error(
                    "Symbol Ingestion Failed | symbol=%s | exception=%s | message=%s",
                    symbol,
                    type(result).__name__,
                    str(result)
                )

            else:
                successful[symbol.ticker] = result
    
        return IngestionResult(
            successful=successful,
            failed=failed
        )