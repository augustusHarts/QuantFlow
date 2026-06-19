from shared.utils.logger import get_logger
from storage.repositories.data_repository import DataRepository
from shared.config.storage_config import DATASET_DIR
from pipelines.preprocessing.pipeline import PreprocessingPipeline
from services.preprocessing.validators.preprocessor_validator import PreprocessorValidator
from services.preprocessing.preprocessors.yahoo_preprocessor import YahooPreprocessor
from services.preprocessing.aggregators.preprocessor_aggregator import PreprocessorAggregator

def main():
    pipeline_logger = get_logger('Preprocessing Pipeline')    

    repository = DataRepository(root_dir=DATASET_DIR)
    
    preprocessor = YahooPreprocessor(
        pipeline_logger.getChild('YahooPreprocessor'),
        validator = PreprocessorValidator()
    )

    aggregator = PreprocessorAggregator(pipeline_logger.getChild('PreprocessorAggregator'))

    pipeline = PreprocessingPipeline(
        logger=pipeline_logger,
        preprocessor=preprocessor,
        aggregator=aggregator,
        repository=repository
    )

    pipeline.run()

if __name__ == '__main__':
    main()