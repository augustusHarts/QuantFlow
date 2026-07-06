from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class PriceRecord:
    timestamp: datetime
    open: float | None
    low: float | None
    high: float | None
    close: float | None
    adj_close: float | None
    volume: int | None

@dataclass(slots=True)
class FeatureRecord:
    timestamp: datetime
    return_1d: float | None
    log_return: float | None
    high_low_range: float | None
    volume_change: float | None
    rolling_std_20: float | None
    sma_5: float | None
    sma_20: float | None
    sma_50: float | None
    close_vs_sma20: float | None
    close_vs_sma50: float | None
    day_of_week: int
    month: int
    quarter: int

@dataclass(slots=True)
class FeatureEngineeredSymbol:
    prices: list[PriceRecord]
    features: list[FeatureRecord]
    