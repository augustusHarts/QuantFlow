from shared.models.ingestion_models import MarketSymbol
from shared.enums.assettype import AssetType

SYMBOLS = [

    MarketSymbol(
        ticker="AAPL",
        asset_type=AssetType.EQUITY
    ),

    MarketSymbol(
        ticker="MSFT",
        asset_type=AssetType.EQUITY
    ),

    MarketSymbol(
        ticker="BTC-USD",
        asset_type=AssetType.CRYPTO
    )
]