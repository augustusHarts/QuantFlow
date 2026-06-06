from dataclasses import dataclass
from shared.enums.pipelinestatus import PipelineStatus

@dataclass
class PipelineRun:
    status: PipelineStatus
    total_symbols: int
    successful_symbols: int
    failed_symbols: int