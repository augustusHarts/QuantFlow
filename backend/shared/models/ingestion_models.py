from dataclasses import dataclass
from datetime import datetime
from aiohttp import ClientTimeout
from shared.enums.datasource import DataSource
from shared.enums.assettype import AssetType

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
    source: DataSource = DataSource.YAHOO

@dataclass(frozen=True, slots=True)
class MarketSymbol:
    ticker: str
    asset_type: AssetType

@dataclass
class HistoricalPrice:
    symbol: str
    asset_type: AssetType
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int