import pytest
import asyncio
from shared.exceptions.ingestion_exceptions import (
    YahooRateLimitError,
    YahooInvalidResponseError,
)
from aiohttp import ClientResponseError
from unittest.mock import Mock
from shared.config.ingestion_config import DEFAULT_HEADERS
from shared.enums.datasource import DataSource


class MockResponse:
    def __init__(self, status=200, json_data=None):
        self.status = status
        self._json_data = json_data or {}

    async def json(self):
        return self._json_data

    def raise_for_status(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


# --------------------------------------------------
# Success
# --------------------------------------------------
@pytest.mark.asyncio
async def test_fetch_success(provider, validator):

    payload = {"chart": {"result": [{}]}}

    session = Mock()

    session.get.return_value = MockResponse(status=200, json_data=payload)

    result = await provider.fetch("AAPL", session)

    assert result == payload

    validator.validate.assert_called_once_with(payload)


# --------------------------------------------------
# Rate limit
# --------------------------------------------------
@pytest.mark.asyncio
async def test_rate_limit(provider):

    session = Mock()

    session.get.return_value = MockResponse(status=429)

    with pytest.raises(YahooRateLimitError):
        await provider.fetch("AAPL", session)


# --------------------------------------------------
# Invalid Response
# --------------------------------------------------
@pytest.mark.asyncio
async def test_invalid_response(provider, validator):

    validator.validate.side_effect = YahooInvalidResponseError("bad payload")

    session = Mock()

    session.get.return_value = MockResponse(status=200, json_data={})

    with pytest.raises(YahooInvalidResponseError):
        await provider.fetch("AAPL", session)


# --------------------------------------------------
# Timeout Retries
# --------------------------------------------------
@pytest.mark.asyncio
async def test_timeout_retries(provider):

    session = Mock()

    session.get.side_effect = asyncio.TimeoutError()

    with pytest.raises(asyncio.TimeoutError):
        await provider.fetch("AAPL", session)


# --------------------------------------------------
# HTTP Error
# --------------------------------------------------
class MockHttpErrorResponse(MockResponse):
    def raise_for_status(self):

        raise ClientResponseError(request_info=Mock(), history=(), status=500)


@pytest.mark.asyncio
async def test_http_error(provider):

    session = Mock()

    session.get.return_value = MockHttpErrorResponse()

    with pytest.raises(ClientResponseError):
        await provider.fetch("AAPL", session)


# --------------------------------------------------
# Build Parameter
# --------------------------------------------------
def test_build_params(provider):

    params = provider._build_params()

    assert params == {"range": "1y", "interval": "1d"}


# --------------------------------------------------
# Build Header
# --------------------------------------------------
def test_build_headers(provider):

    headers = provider._build_headers()

    assert "User-Agent" in headers


def test_source(provider):
    assert provider.source == DataSource.YAHOO


def test_provider_configuration(provider, config):
    assert provider.config == config


def test_build_headers_returns_copy(provider):
    headers = provider._build_headers()

    assert headers == DEFAULT_HEADERS

    assert headers is not DEFAULT_HEADERS


def test_build_params_uses_config(provider, config):
    params = provider._build_params()

    assert params["range"] == config.range
    assert params["interval"] == config.interval
