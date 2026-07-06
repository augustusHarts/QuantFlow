from shared.decorators.logging import log_stage
from shared.models.preprocessing_model import PreprocessingResult, PreprocessedSymbol
from services.preprocessing.interfaces.aggregator import Aggregator
from shared.models.ingestion_models import DataSource


class PreprocessorAggregator(Aggregator):
    def __init__(self, logger):
        self.logger = logger

    @log_stage("Aggregating Results")
    def aggregate(
        self,
        symbols: list[tuple[DataSource, str]],
        results: list[PreprocessedSymbol | BaseException],
    ) -> PreprocessingResult:

        successful: dict[tuple, PreprocessedSymbol] = {}
        failed: dict[tuple, BaseException] = {}

        for (provider, symbol), result in zip(symbols, results):
            if isinstance(result, BaseException):
                failed[(provider, symbol)] = result

                
                self.logger.error(
                    "Symbol Preprocessing Failed | symbol=%s | exception=%s | message=%s",
                    symbol,
                    type(result).__name__,
                    str(result),
                )

            else:
                successful[(provider, symbol)] = result

        return PreprocessingResult(successful=successful, failed=failed)
