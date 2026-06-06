from services.ingestion.interfaces.preprocessor import Preprocessor
from logging import Logger

class YahooPreprocessor(Preprocessor):

    def __init__(
        self,
        logger: Logger
    ):
        self.logger = logger

    def preprocess(self):
        ...

# flatten json
# convert timestamp
# Remove duplicates
# Sort
# Validate again