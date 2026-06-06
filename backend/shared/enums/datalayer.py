from enum import StrEnum

class DataLayer(StrEnum):
    RAW = "raw"
    PROCESSED = "processed"
    CURATED = "curated"