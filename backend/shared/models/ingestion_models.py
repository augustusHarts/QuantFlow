from dataclasses import dataclass
from typing import Any
from aiohttp import ClientTimeout
from shared.enums.datasource import DataSource
from shared.enums.assettype import AssetType
from shared.enums.datalayer import DataLayer

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

@dataclass(slots=True)
class SaveRequest:
    layer: DataLayer
    provider: DataSource
    key: str
    payload: dict[str, Any]