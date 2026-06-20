from services.preprocessing.interfaces.preprocessor import Preprocessor
from services.preprocessing.validators.preprocessor_validator import (
    PreprocessorValidator,
)
from shared.models.preprocessing_model import PreprocessedSymbol, PriceRecord, MetaData
from logging import Logger
from shared.enums.datasource import DataSource
from shared.enums.assettype import AssetType
from datetime import datetime, UTC


class YahooPreprocessor(Preprocessor):
    def __init__(self, logger: Logger, validator: PreprocessorValidator):
        self.logger = logger
        self.validator = validator

    def _process_meta(self, meta: dict) -> MetaData:

        return MetaData(
            symbol=meta["symbol"],
            asset_type=AssetType(meta["instrumentType"].lower()),
            currency=meta["currency"],
            exchange=meta["exchangeName"],
            timezone=meta["timezone"],
            source=DataSource.YAHOO,
        )

    def _process_records(self, result: dict) -> list[PriceRecord]:

        timestamp = result["timestamp"]

        indicators = result["indicators"]
        opens: list[float] = indicators["quote"][0]["open"]
        lows: list[float] = indicators["quote"][0]["low"]
        highs: list[float] = indicators["quote"][0]["high"]
        closes: list[float] = indicators["quote"][0]["close"]
        volumes: list[int] = indicators["quote"][0]["volume"]
        adj_closes: list[float] = indicators["adjclose"][0]["adjclose"]

        lengths = {
            "timestamp": len(timestamp),
            "opens": len(opens),
            "lows": len(lows),
            "highs": len(highs),
            "closes": len(closes),
            "adj_close": len(adj_closes),
            "volumes": len(volumes),
        }

        self.validator.validate_record_length(lengths)

        records = [
            PriceRecord(
                timestamp=datetime.fromtimestamp(ts, tz=UTC),
                open=open_price,
                low=low_price,
                high=high_price,
                close=close_price,
                adj_close=adj_close_price,
                volume=volume,
            )
            for ts, open_price, low_price, high_price, close_price, adj_close_price, volume in zip(
                timestamp, opens, lows, highs, closes, adj_closes, volumes
            )
            if all(value is not None for value in (open_price, high_price, low_price, close_price))
        ]

        sorted_records = sorted(records, key=lambda record: record.timestamp)

        unique_records = self.validator.remove_duplicate_records(sorted_records)

        return unique_records

    def preprocess(self, data: dict) -> PreprocessedSymbol:

        raw_meta = data["chart"]["result"][0]["meta"]
        processed_meta = self._process_meta(raw_meta)
        self.logger.debug("Preprocessed Meta Data for symbol=%s", processed_meta.symbol)

        raw_records = data["chart"]["result"][0]
        processed_records = self._process_records(raw_records)
        self.logger.debug(
            "Preprocessed symbol=%s | records=%d",
            processed_meta.symbol,
            len(processed_records),
        )

        symbol = PreprocessedSymbol(meta=processed_meta, records=processed_records)

        self.validator.validate(symbol)

        return symbol
