from shared.models.preprocessing_model import PriceRecord, PreprocessedSymbol, MetaData 

class PreprocessorValidator:

    def validate_record_length(
        self,
        lengths: dict[str, int]
    ) -> None:
        record_length = set(lengths.values())

        if len(record_length) != 1:
            raise ValueError(f'Record\'s length mismatch: {record_length}')

    def remove_duplicate_records(
        self,
        records: list[PriceRecord]
    ) -> list[PriceRecord]:
        seen_timestamp = set()
        unique_records = []

        for record in records:
            if record.timestamp not in seen_timestamp:
                seen_timestamp.add(record.timestamp)
                unique_records.append(record)

        return unique_records

    def validate(
        self,
        symbol: PreprocessedSymbol
    ) -> None:

        self.validate_metadata(symbol.meta)
        self.validate_records_exist(symbol.records)
        self.validate_duplicate_timestamps(symbol.records)
        self.validate_ohlc(symbol.records)

    def validate_metadata(
        self,
        meta: MetaData
    ) -> None:

        if not meta.symbol:
            raise ValueError("Missing symbol")

        if not meta.currency:
            raise ValueError("Missing currency")

        if not meta.exchange:
            raise ValueError("Missing exchange")

    def validate_records_exist(
        self,
        records: list[PriceRecord]
    ) -> None:

        if not records:
            raise ValueError("No records found")

    def validate_duplicate_timestamps(
        self,
        records: list[PriceRecord]
    ) -> None:

        timestamps = [
            record.timestamp
            for record in records
        ]

        if len(timestamps) != len(set(timestamps)):
            raise ValueError(
                "Duplicate timestamps detected"
            )

    def validate_ohlc(
        self,
        records: list[PriceRecord]
    ) -> None:

        for record in records:

            if record.high is None or record.low is None:
                raise ValueError(
                    f"Missing high/low on {record.timestamp}"
                )

            if record.high < record.low:
                raise ValueError(
                    f"Invalid OHLC on {record.timestamp}"
                )

            if record.open is not None:

                if record.open > record.high:
                    raise ValueError(
                        f"Open greater than high on {record.timestamp}"
                    )

                if record.open < record.low:
                    raise ValueError(
                        f"Open lower than low on {record.timestamp}"
                    )

            if record.close is not None:

                if record.close > record.high:
                    raise ValueError(
                        f"Close greater than high on {record.timestamp}"
                    )

                if record.close < record.low:
                    raise ValueError(
                        f"Close lower than low on {record.timestamp}"
                    )