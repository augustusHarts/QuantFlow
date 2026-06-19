from abc import ABC, abstractmethod
from shared.models.preprocessing_model import PreprocessedSymbol
import pandas as pd

class Preprocessor(ABC):

    @abstractmethod
    def preprocess(
        self,
        data: dict
    ) -> PreprocessedSymbol:
        ...