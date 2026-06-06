from typing import Any

from shared.decorators.logging import log_stage
from shared.models.ingestion_models import IngestionResult
from services.ingestion.interfaces.processor import Processor


class YahooProcessor(Processor):

    def __init__(self, logger):
        self.logger = logger

    @log_stage("Processing Results")
    def process(
        self,
        symbols: list[str],
        results: list[dict[str, Any] | BaseException]
    ) -> IngestionResult:

        successful: dict[str, dict[str, Any]] = {}
        failed: dict[str, BaseException] = {}

        for symbol, result in zip(symbols, results):

            if isinstance(result, BaseException):

                failed[symbol] = result

                self.logger.error(
                    "Symbol Ingestion Failed: \n\tsymbol: %s \n\texception: %s \n\tmessage: %s",
                    symbol,
                    type(result).__name__,
                    str(result)
                )

            else:

                successful[symbol] = result


        self.logger.info(
            'Ingestion Summmary: \n\trequested: %d \n\tsuccessful: %d \n\tfailed: %d', 
            len(symbols), 
            len(successful), 
            len(failed)
        )
    
        return IngestionResult(
            successful=successful,
            failed=failed
        )