from abc import ABC, abstractmethod

import pandas as pd

class Transformation(ABC):

    @abstractmethod
    def transform(
        self,
        df
    ) -> pd.DataFrame:
        ...