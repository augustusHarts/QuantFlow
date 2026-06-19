from dataclasses import dataclass
from datetime import datetime
from shared.enums.assettype import AssetType
from shared.enums.datasource import DataSource
from shared.enums.datalayer import DataLayer

@dataclass(slots=True)
class SaveRequest:
    layer: DataLayer
    provider: DataSource
    

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
class MetaData:
    symbol: str
    asset_type: AssetType
    currency: str
    exchange: str
    timezone: str
    source: DataSource

@dataclass(slots=True)
class PreprocessedSymbol:
    meta: MetaData
    records: list[PriceRecord]

@dataclass(slots=True)
class PreprocessingResult:
    successful: dict[tuple, PreprocessedSymbol]
    failed: dict[tuple, BaseException]