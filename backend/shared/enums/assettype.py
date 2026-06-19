from enum import StrEnum

class AssetType(StrEnum):
    EQUITY = "equity"
    CRYPTO = "cryptocurrency"
    ETF = "etf"
    FOREX = "forex"
    COMMODITY = "commodity"