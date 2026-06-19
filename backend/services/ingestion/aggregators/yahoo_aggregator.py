from typing import Any
from shared.decorators.logging import log_stage
from shared.models.ingestion_models import Result
from services.ingestion.interfaces.aggregator import Aggregator
from shared.models.ingestion_models import MarketSymbol

class YahooAggregator(Aggregator):

    def __init__(self, logger):
        self.logger = logger

    @log_stage("Aggregating Results")
    def aggregate(
        self,
        symbols: list[MarketSymbol],
        results: list[dict[str, Any] | BaseException]
    ) -> Result:

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
    
        return Result(
            successful=successful,
            failed=failed
        )