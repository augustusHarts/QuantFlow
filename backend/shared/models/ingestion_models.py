from dataclasses import dataclass
from datetime import datetime

@dataclass
class IngestionResult:
    successful: dict[str, dict]
    failed: dict[str, BaseException]

@dataclass
class HistoricalPrice:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int