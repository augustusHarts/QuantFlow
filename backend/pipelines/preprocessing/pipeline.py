from logging import Logger
from shared.enums.pipelinestatus import PipelineStatus
from shared.models.preprocessing_model import PreprocessingResult
from storage.repositories.data_repository import DataRepository
from shared.models.preprocessing_model import SaveRequest
from pipelines.preprocessing.tasks import persist_processed_data
from services.preprocessing.interfaces.preprocessor import Preprocessor
from pipelines.preprocessing.tasks import get_key_list, get_pipeline_status
from pipelines.preprocessing.config import BASE_LAYER
from services.preprocessing.interfaces.aggregator import Aggregator
from concurrent.futures import ThreadPoolExecutor

class PreprocessingPipeline:

    def __init__(
        self,
        logger: Logger,
        preprocessor: Preprocessor,
        aggregator: Aggregator,
        repository: DataRepository
    ):
        self.logger = logger
        self.preprocessor = preprocessor
        self.aggregator = aggregator
        self.repository = repository
        self.status = PipelineStatus.PENDING

    def run(self) -> PreprocessingResult:
    
        keys = get_key_list(
            self.repository, 
            BASE_LAYER
        )

        if not keys:
            self.logger.warning('No provider and keys founds')
            return PreprocessingResult(
                successful={},
                failed={}
            )

        self.status = PipelineStatus.RUNNING
        
        self.logger.info(
            "Preprocessing Started | source=%s | status=%s | total=%d",
            keys.keys(),
            self.status.value,
            sum(len(symbol) for symbol in keys.values())
        )

        symbols = []
        results = []

        for provider, provider_symbols in keys.items():
            for symbol in provider_symbols:
                symbols.append((provider, symbol))
                try:
                    raw_data = self.repository.load(
                        BASE_LAYER,
                        provider,
                        symbol
                    )
                    results.append(
                        self.preprocessor.preprocess(
                            raw_data
                        )
                    )
                except Exception as exc:
                    results.append(exc)

        aggregated = self.aggregator.aggregate(
            symbols=symbols,
            results=results
        )
        
        persist_processed_data(
            repository=self.repository,
            data=aggregated.successful
        )

        self.status = get_pipeline_status(
            successful_count=len(aggregated.successful),
            failed_count=len(aggregated.failed)
        )

        self.logger.info(
            "Preprocessing Completed | status=%s | total=%d | successful=%d | failed=%d",
            self.status.value,
            sum(len(symbol) for symbol in keys.values()),
            len(aggregated.successful),
            len(aggregated.failed)
        )

        return aggregated