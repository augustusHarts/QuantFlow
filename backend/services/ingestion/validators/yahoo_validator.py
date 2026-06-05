from shared.exceptions.ingestion_exceptions import YahooInvalidResponseError

class YahooValidator:

    def validate(
        self,
        payload: dict
    ) -> None:

        chart = payload.get("chart", {})

        if chart.get("error"):
            raise YahooInvalidResponseError()

        result = chart.get("result")

        if not result:
            raise YahooInvalidResponseError()

        result = result[0]

        if "timestamp" not in result:
            raise YahooInvalidResponseError()

        indicators = result.get(
            "indicators",
            {}
        )

        quote = indicators.get("quote")

        if not quote:
            raise YahooInvalidResponseError()

        
        quote = quote[0]

        required_fields = [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        for field in required_fields:

            if field not in quote:
                raise YahooInvalidResponseError(
                    f"Missing field: {field}"
                )