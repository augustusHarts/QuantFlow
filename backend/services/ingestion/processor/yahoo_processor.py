from typing import Any

from shared.models.ingestion_models import IngestionResult


class YahooProcessor:

    def __init__(
        self,
        logger
    ):
        self.logger = logger
    
    def process_results(
            self,
            symbols: list[str],
            results: list[Any | BaseException],
        ) -> IngestionResult:
        
            successful = {}
            failed = {}
            
            for symbol, result in zip(
                symbols,
                results
            ):
                if isinstance(
                    result,
                    Exception
                ):
                    failed[symbol] = result
                    self.logger.error(
                        'symbol_failed',
                        extra={
                            'symbol': symbol,
                            'error': str(result),
                            'exception_type': type(result).__name__
                        }
                    )

                else:  
                    successful[symbol] = result

            return IngestionResult(
                successful=successful,
                failed=failed 
            )