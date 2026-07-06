from logging import Logger
from shared.enums.pipelinestatus import PipelineStatus
from shared.enums.datasource import DataSource
from storage.interfaces.repository import Repository
from shared.models.engineering_models import FeatureEngineeredSymbol
from pipelines.feature_engineering.tasks import get_symbol_list
from pipelines.feature_engineering.config import BASE_LAYER

class FeatureEngineerPipeline:

    def __init__(
        self,
        logger: Logger,
        engineer,
        repository: Repository
    ):
        self.logger = logger
        self.engineer = engineer
        self.repository = repository
        self.status = PipelineStatus.PENDING

    def run(self):

        symbols_by_provider  = get_symbol_list(self.repository, BASE_LAYER)

        if not symbols_by_provider :
            self.logger.warning("No provider and keys founds")
            # return FeatureEngineeringResult(successful={}, failed={})

        self.status = PipelineStatus.RUNNING

        self.logger.info(
            "Preprocessing Started | source=%s | status=%s | total=%d",
            symbols_by_provider.keys(),
            self.status.value,
            sum(len(symbol) for symbol in symbols_by_provider .values()),
        )

        symbols: list[tuple[DataSource, str]] = []
        results: list[FeatureEngineeredSymbol | BaseException] = []

        for provider, provider_symbols in symbols_by_provider.items():
            for symbol in provider_symbols:
                symbols.append((provider, symbol))
                try:
                    processed_data = self.repository.load(BASE_LAYER, provider, symbol)
                    results.append(self.engineer.engineer(processed_data))
                except Exception as exc:
                    results.append(exc)
  
         
                     