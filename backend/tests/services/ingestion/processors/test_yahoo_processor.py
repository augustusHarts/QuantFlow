from shared.exceptions.ingestion_exceptions import (
    YahooInvalidResponseError
)

# --------------------------------------------------
# Success
# --------------------------------------------------
def test_all_successful(processor):

    symbols = [
        "AAPL",
        "MSFT"
    ]

    results = [
        {"price": 100},
        {"price": 200}
    ]

    output = processor.process(
        symbols,
        results
    )

    assert len(output.successful) == 2
    assert len(output.failed) == 0

    assert output.successful["AAPL"] == {"price": 100}
    assert output.successful["MSFT"] == {"price": 200}

# --------------------------------------------------
# Failures
# --------------------------------------------------
def test_all_failed(processor):

    symbols = [
        "AAPL",
        "MSFT"
    ]

    results = [
        YahooInvalidResponseError("bad"),
        YahooInvalidResponseError("bad")
    ]

    output = processor.process(
        symbols,
        results
    )

    assert len(output.successful) == 0
    assert len(output.failed) == 2

    assert isinstance(
        output.failed["AAPL"],
        YahooInvalidResponseError
    )

    assert isinstance(
        output.failed["MSFT"],
        YahooInvalidResponseError
    )

# --------------------------------------------------
# Mixed
# --------------------------------------------------
def test_mixed_results(processor):

    symbols = [
        "AAPL",
        "MSFT",
        "GOOG"
    ]

    results = [
        {"price": 100},
        YahooInvalidResponseError("bad"),
        {"price": 300}
    ]

    output = processor.process(
        symbols,
        results
    )

    assert len(output.successful) == 2
    assert len(output.failed) == 1

    assert "AAPL" in output.successful
    assert "GOOG" in output.successful

    assert "MSFT" in output.failed

# --------------------------------------------------
# Empty Input
# --------------------------------------------------
def test_empty_input(processor):

    output = processor.process(
        [],
        []
    )

    assert output.successful == {}
    assert output.failed == {}

# --------------------------------------------------
# Logger 
# --------------------------------------------------
def test_logs_failure(
    processor,
    caplog
):

    symbols = ["AAPL"]

    results = [
        YahooInvalidResponseError("bad")
    ]

    processor.process(
        symbols,
        results
    )

    assert "Symbol Ingestion Failed" in caplog.text