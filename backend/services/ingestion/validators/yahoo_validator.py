from typing import Any, Final

from shared.exceptions.ingestion_exceptions import YahooInvalidResponseError


class YahooValidator:
    """
    Validates Yahoo Finance chart API responses
    before they enter the processing pipeline.
    """

    REQUIRED_FIELDS: Final[tuple[str, ...]] = (
        "open",
        "high",
        "low",
        "close",
        "volume",
    )

    PRICE_FIELDS: Final[tuple[str, ...]] = (
        "open",
        "high",
        "low",
        "close",
    )

    def validate(self, payload: dict[str, Any]) -> None:

        # --------------------------------------------------
        # Payload
        # --------------------------------------------------

        if not isinstance(payload, dict):
            raise YahooInvalidResponseError("Payload must be a dictionary")

        charts = payload.get("chart")

        if not isinstance(charts, dict):
            raise YahooInvalidResponseError("chart must be a dictionary")

        if charts.get("error"):
            raise YahooInvalidResponseError("Yahoo returned an error")

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        results = charts.get("result")

        if not isinstance(results, list) or not results:
            raise YahooInvalidResponseError("Missing result")

        result = results[0]

        if not isinstance(result, dict):
            raise YahooInvalidResponseError("result must contain dictionaries")

        # --------------------------------------------------
        # Timestamp
        # --------------------------------------------------

        timestamp = result.get("timestamp")

        if not isinstance(timestamp, list) or not timestamp:
            raise YahooInvalidResponseError("Missing timestamp")

        if not all(ts is None or isinstance(ts, int) for ts in timestamp):
            raise YahooInvalidResponseError("Timestamp must contain integers")

        expected_length = len(timestamp)

        # --------------------------------------------------
        # Indicators
        # --------------------------------------------------

        indicators = result.get("indicators")

        if not isinstance(indicators, dict):
            raise YahooInvalidResponseError("indicators must be a dictionary")

        # --------------------------------------------------
        # Quote
        # --------------------------------------------------

        quotes = indicators.get("quote")

        if not isinstance(quotes, list) or not quotes:
            raise YahooInvalidResponseError("Quote must be a non-empty list")

        quote = quotes[0]

        if not isinstance(quote, dict):
            raise YahooInvalidResponseError("Quote must contain a dictionary")

        # Required fields
        for field in self.REQUIRED_FIELDS:
            values = quote.get(field)

            if values is None:
                raise YahooInvalidResponseError(f"{field} is missing")

            if not isinstance(values, list):
                raise YahooInvalidResponseError(f"{field} must be a list")

            if len(values) != expected_length:
                raise YahooInvalidResponseError(f"{field} length mismatch")

        # Price fields
        for field in self.PRICE_FIELDS:
            if not all(
                value is None or isinstance(value, (int, float))
                for value in quote[field]
            ):
                raise YahooInvalidResponseError(f"{field} contains invalid values")

        # Volume
        if not all(
            value is None or isinstance(value, int) for value in quote["volume"]
        ):
            raise YahooInvalidResponseError("volume contains invalid values")

        # --------------------------------------------------
        # Adj Close
        # --------------------------------------------------

        adj_closes = indicators.get("adjclose")

        if not isinstance(adj_closes, list) or not adj_closes:
            raise YahooInvalidResponseError("Missing adjclose")

        adj_close = adj_closes[0]

        if not isinstance(adj_close, dict):
            raise YahooInvalidResponseError("adjclose must contain a dictionary")

        adj_close_values = adj_close.get("adjclose")

        if not isinstance(adj_close_values, list):
            raise YahooInvalidResponseError("adjclose must be a list")

        if len(adj_close_values) != expected_length:
            raise YahooInvalidResponseError("adjclose length mismatch")

        if not all(
            value is None or isinstance(value, (int, float))
            for value in adj_close_values
        ):
            raise YahooInvalidResponseError("adjclose contains invalid values")
