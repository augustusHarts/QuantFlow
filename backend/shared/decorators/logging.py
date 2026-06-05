from functools import wraps
import inspect
import time
from shared.utils.logger import get_logger


def log_stage(name=None):

    def decorator(func):

        if inspect.iscoroutinefunction(func):
        
            @wraps(func)
            async def async_wrapper(*args, **kwargs):

                display_name = name or func.__name__

                extra={}
                if "symbol" in kwargs:
                    extra["symbol"] = kwargs["symbol"]

                logger = getattr(
                    args[0], 
                    "logger", 
                    None
                )

                if logger is None:
                    raise RuntimeError(
                        f"{func.__qualname__} requires self.logger"
                    )

                logger.info(
                    "Started %s",
                    display_name,
                    extra=extra
                )

                start = time.perf_counter()

                try:

                    result = await func(*args, **kwargs)

                    duration = (
                        time.perf_counter()
                        - start
                    )

                    logger.info(
                        "Completed %s in %.2f sec",
                        display_name,
                        duration
                    )

                    return result

                except Exception:

                    duration = (
                        time.perf_counter()
                        - start
                    )

                    logger.exception(
                        "Failed %s after %.2f sec",
                        display_name,
                        duration,
                        extra=extra
                    )

                    raise

            return async_wrapper

        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                display_name = name or func.__name__
                
                extra={}
                if "symbol" in kwargs:
                    extra["symbol"] = kwargs["symbol"]

                logger = getattr(
                    args[0], 
                    "logger", 
                    None
                )

                if logger is None:
                    raise RuntimeError(
                        f"{func.__qualname__} requires self.logger"
                    )

                logger.info(
                    "Started %s",
                    display_name,
                    extra=extra
                )

                start = time.perf_counter()

                try:

                    result = func(
                        *args,
                        **kwargs
                    )

                    duration = (
                        time.perf_counter()
                        - start
                    )

                    logger.info(
                        "Completed %s in %.2f sec",
                        display_name,
                        duration,
                        extra=extra
                    )

                    return result

                except Exception:

                    duration = (
                        time.perf_counter()
                        - start
                    )

                    logger.exception(
                        "Failed %s after %.2f sec",
                        display_name,
                        duration
                    )

                    raise

            return sync_wrapper
    
    return decorator