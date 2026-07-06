from shared.utils.logger import get_logger
from pipelines.feature_engineering.pipeline import FeatureEngineerPipeline
from services.feature_engineering.engineers.yahoo_feature_engineer import YahooFeatureEngineer
from storage.repositories.data_repository import DataRepository
from shared.config.storage_config import DATASET_DIR

def main():
    pipeline_logger = get_logger("Feature Engineering Pipeline")

    engineer = YahooFeatureEngineer(
        pipeline_logger.getChild('YahooFeatureEngineer')
    )

    repository = DataRepository(root_dir=DATASET_DIR)
    
    pipeline = FeatureEngineerPipeline(
        logger=pipeline_logger,
        engineer=engineer,
        repository=repository
    )
    pipeline.run() 
 
if __name__ == '__main__':
    main()