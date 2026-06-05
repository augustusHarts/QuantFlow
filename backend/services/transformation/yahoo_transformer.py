from shared.models.ingestion_models import IngestionResult

class YahooTransformer:

    def __init__(
        self,
        logger
    ):
        self.logger = logger

    def transform(
        self,
        raw_data: IngestionResult
    ):
        pass