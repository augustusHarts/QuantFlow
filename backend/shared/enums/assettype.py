from enum import StrEnum

class AssetType(StrEnum):
    EQUITY = "equity"
    CRYPTO = "crypto"
    ETF = "etf"
    FOREX = "forex"
    COMMODITY = "commodity"