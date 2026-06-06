from dataclasses import dataclass
from datetime import datetime
from aiohttp import ClientTimeout

@dataclass
class IngestionResult:
    successful: dict[str, dict]
    failed: dict[str, BaseException]

@dataclass(frozen=True, slots=True)
class YahooConfig:
    base_url: str
    interval: str
    range: str
    timeout: ClientTimeout

@dataclass
class HistoricalPrice:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int