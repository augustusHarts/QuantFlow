from logging import Logger
from typing import Any

class YahooFeatureEngineer:

    def __init__(
        self,
        logger: Logger
    ):
        self.logger = logger

    def engineer(
        self,
        data: dict[str, Any]
    ):
        ... 