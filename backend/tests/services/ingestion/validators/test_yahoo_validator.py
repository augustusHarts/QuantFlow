import pytest

from services.ingestion.validators.yahoo_validator import YahooValidator

@pytest.fixture
def validator():
    return YahooValidator()

def test_validator_instance(validator):
    assert isinstance(
        validator,
        YahooValidator
    )