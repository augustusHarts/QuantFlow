from dataclasses import dataclass
from datetime import datetime

@dataclass
class IngestionResult:
    successful: dict
    failed: dict

@dataclass
class HistoricalPrice:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int