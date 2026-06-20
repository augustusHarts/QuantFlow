from dataclasses import dataclass
from datetime import datetime
from shared.enums.pipelinestatus import PipelineStatus
from shared.enums.assettype import AssetType
from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
from typing import Any


@dataclass(slots=True)
class SaveRequest:
    layer: DataLayer
    provider: DataSource
    key: str
    payload: Any


@dataclass
class PipelineRun:
    status: PipelineStatus
    total_symbols: int
    successful_symbols: int
    failed_symbols: int


@dataclass
class DatasetMetaData:
    symbol: str
    provider: str
    asset_type: AssetType
    symbol_last_timestamp: datetime
    raw_updated_at: datetime
    processed_updated_at: datetime
    record_count: int
    pipeline_status: PipelineStatus
