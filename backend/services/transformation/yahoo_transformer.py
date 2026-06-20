from services.ingestion.interfaces.transformation import Transformation

import pandas as pd


class YahooTransformer(Transformation):
    def __init__(self, logger):
        self.logger = logger

    def transform(self, df) -> pd.DataFrame:

        return pd.DataFrame()
