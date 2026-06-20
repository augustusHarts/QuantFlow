import pytest
from copy import deepcopy

from shared.exceptions.ingestion_exceptions import YahooInvalidResponseError


# --------------------------------------------------
# Payload
# --------------------------------------------------
def test_valid_payload(validator, valid_payload):
    validator.validate(valid_payload)


def test_empty_payload(validator):
    with pytest.raises(YahooInvalidResponseError):
        validator.validate({})


def test_payload_not_dict(validator):
    with pytest.raises(YahooInvalidResponseError, match="Payload must be a dictionary"):
        validator.validate(None)


# --------------------------------------------------
# Charts
# --------------------------------------------------
def test_chart_not_dict(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"] = []

    with pytest.raises(YahooInvalidResponseError, match="chart must be a dictionary"):
        validator.validate(payload)


def test_chart_error(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["error"] = {"code": "Bad Request"}

    with pytest.raises(YahooInvalidResponseError, match="Yahoo returned an error"):
        validator.validate(payload)


# --------------------------------------------------
# Results
# --------------------------------------------------
def test_missing_result(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"] = []

    with pytest.raises(YahooInvalidResponseError, match="Missing result"):
        validator.validate(payload)


def test_result_not_list(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"] = "bad"

    with pytest.raises(YahooInvalidResponseError, match="Missing result"):
        validator.validate(payload)


def test_result_not_dict(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"] = [123]

    with pytest.raises(
        YahooInvalidResponseError, match="result must contain dictionaries"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Timestamp
# --------------------------------------------------
def test_missing_timestamp(validator, valid_payload):
    payload = deepcopy(valid_payload)
    del payload["chart"]["result"][0]["timestamp"]

    with pytest.raises(YahooInvalidResponseError, match="Missing timestamp"):
        validator.validate(payload)


def test_timestamp_not_list(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["timestamp"] = "bad"

    with pytest.raises(YahooInvalidResponseError, match="Missing timestamp"):
        validator.validate(payload)


def test_invalid_timestamp_type(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["timestamp"] = [1, "bad", 3]

    with pytest.raises(
        YahooInvalidResponseError, match="Timestamp must contain integers"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Indicators
# --------------------------------------------------
def test_indicators_not_dict(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"] = []

    with pytest.raises(
        YahooInvalidResponseError, match="indicators must be a dictionary"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Quotes
# --------------------------------------------------
def test_missing_quote(validator, valid_payload):
    payload = deepcopy(valid_payload)
    del payload["chart"]["result"][0]["indicators"]["quote"]

    with pytest.raises(
        YahooInvalidResponseError, match="Quote must be a non-empty list"
    ):
        validator.validate(payload)


def test_quote_not_list(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"] = {}

    with pytest.raises(
        YahooInvalidResponseError, match="Quote must be a non-empty list"
    ):
        validator.validate(payload)


def test_quote_not_dict(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"] = [123]

    with pytest.raises(
        YahooInvalidResponseError, match="Quote must contain a dictionary"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Required Fields
# --------------------------------------------------
@pytest.mark.parametrize("field", ["open", "high", "low", "close", "volume"])
def test_missing_required_field(validator, valid_payload, field):
    payload = deepcopy(valid_payload)
    del payload["chart"]["result"][0]["indicators"]["quote"][0][field]

    with pytest.raises(YahooInvalidResponseError, match=f"{field} is missing"):
        validator.validate(payload)


@pytest.mark.parametrize("field", ["open", "high", "low", "close", "volume"])
def test_required_field_not_list(validator, valid_payload, field):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"][0][field] = 1

    with pytest.raises(YahooInvalidResponseError, match=f"{field} must be a list"):
        validator.validate(payload)


@pytest.mark.parametrize("field", ["open", "high", "low", "close", "volume"])
def test_length_mismatch(validator, valid_payload, field):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"][0][field] = [1]

    with pytest.raises(YahooInvalidResponseError, match=f"{field} length mismatch"):
        validator.validate(payload)


# --------------------------------------------------
# Price Fields
# --------------------------------------------------
@pytest.mark.parametrize("field", ["open", "high", "low", "close"])
def test_invalid_price_type(validator, valid_payload, field):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"][0][field] = [1.0, "bad", 3.0]

    with pytest.raises(
        YahooInvalidResponseError, match=f"{field} contains invalid values"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Volume
# --------------------------------------------------
def test_invalid_volume_type(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["quote"][0]["volume"] = [
        100,
        "bad",
        300,
    ]

    with pytest.raises(
        YahooInvalidResponseError, match="volume contains invalid values"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Adjclose
# --------------------------------------------------
def test_missing_adjclose(validator, valid_payload):
    payload = deepcopy(valid_payload)
    del payload["chart"]["result"][0]["indicators"]["adjclose"]

    with pytest.raises(YahooInvalidResponseError, match="Missing adjclose"):
        validator.validate(payload)


def test_adjclose_not_list(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["adjclose"] = {}

    with pytest.raises(YahooInvalidResponseError, match="Missing adjclose"):
        validator.validate(payload)


def test_adjclose_item_not_dict(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["adjclose"] = [123]

    with pytest.raises(
        YahooInvalidResponseError, match="adjclose must contain a dictionary"
    ):
        validator.validate(payload)


def test_adjclose_values_not_list(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["adjclose"] = [{"adjclose": 123}]

    with pytest.raises(YahooInvalidResponseError, match="adjclose must be a list"):
        validator.validate(payload)


def test_adjclose_length_mismatch(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["adjclose"] = [{"adjclose": [1]}]

    with pytest.raises(YahooInvalidResponseError, match="adjclose length mismatch"):
        validator.validate(payload)


def test_adjclose_invalid_type(validator, valid_payload):
    payload = deepcopy(valid_payload)
    payload["chart"]["result"][0]["indicators"]["adjclose"] = [
        {"adjclose": [1.0, "bad", 3.0]}
    ]

    with pytest.raises(
        YahooInvalidResponseError, match="adjclose contains invalid values"
    ):
        validator.validate(payload)


# --------------------------------------------------
# Valid Edge Cases
# --------------------------------------------------
def test_timestamp_allows_none(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["timestamp"] = [1, None, 3]

    validator.validate(payload)


@pytest.mark.parametrize("field", ["open", "high", "low", "close"])
def test_price_field_allows_none(validator, valid_payload, field):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["quote"][0][field] = [1.0, None, 3.0]

    validator.validate(payload)


def test_volume_allows_none(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["quote"][0]["volume"] = [100, None, 300]

    validator.validate(payload)


def test_adjclose_allows_none(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["adjclose"] = [
        {"adjclose": [1.0, None, 3.0]}
    ]

    validator.validate(payload)


# --------------------------------------------------
# Quote Edge Cases
# --------------------------------------------------
def test_quote_empty_list(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["quote"] = []

    with pytest.raises(
        YahooInvalidResponseError, match="Quote must be a non-empty list"
    ):
        validator.validate(payload)


def test_empty_quote_dictionary(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["quote"] = [{}]

    with pytest.raises(YahooInvalidResponseError, match="open is missing"):
        validator.validate(payload)


# --------------------------------------------------
# Adjclose Edge Cases
# --------------------------------------------------
def test_adjclose_empty_list(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["adjclose"] = []

    with pytest.raises(YahooInvalidResponseError, match="Missing adjclose"):
        validator.validate(payload)


def test_adjclose_missing_values(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["adjclose"] = [{}]

    with pytest.raises(YahooInvalidResponseError, match="adjclose must be a list"):
        validator.validate(payload)


def test_volume_zero_allowed(validator, valid_payload):
    payload = deepcopy(valid_payload)

    payload["chart"]["result"][0]["indicators"]["quote"][0]["volume"] = [0, 100, 200]

    validator.validate(payload)
