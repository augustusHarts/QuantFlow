from functools import wraps
from pathlib import Path
import pandas as pd
import inspect

def save_as_csv(path: Path):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            if not isinstance(result, pd.DataFrame):
                return result

            bound = inspect.signature(func).bind(
                *args,
                **kwargs
            )

            symbol = bound.arguments["symbol"]

            file_path = path / f'{symbol}.csv'

            result.to_csv(
                file_path, 
                index=False
            )

            return result

        return wrapper

    return decorator