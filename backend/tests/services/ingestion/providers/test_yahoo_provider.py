import pytest
import asyncio
from shared.exceptions.ingestion_exceptions import (
    YahooRateLimitError,
    YahooInvalidResponseError
)
from aiohttp import ClientResponseError
from unittest.mock import (
    AsyncMock, 
    patch, 
    Mock
)

class MockResponse:

    def __init__(
        self,
        status=200,
        json_data=None
    ):
        self.status = status
        self._json_data = json_data or {}

    async def json(self):
        return self._json_data

    def raise_for_status(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb
    ):
        pass

# --------------------------------------------------
# Success
# --------------------------------------------------
@pytest.mark.asyncio
async def test_fetch_success(
    provider,
    validator
):

    payload = {
        "chart": {
            "result": [{}]
        }
    }

    session = Mock()

    session.get.return_value = MockResponse(
        status=200,
        json_data=payload
    )

    result = await provider.fetch(
        "AAPL",
        session
    )

    assert result == payload

    validator.validate.assert_called_once_with(
        payload
    )

# --------------------------------------------------
# Rate limit
# --------------------------------------------------
@pytest.mark.asyncio
async def test_rate_limit(
    provider
):

    session = Mock()

    session.get.return_value = MockResponse(
        status=429
    )

    with pytest.raises(
        YahooRateLimitError
    ):
        await provider.fetch(
            "AAPL",
            session
        )

# --------------------------------------------------
# Invalid Response
# --------------------------------------------------
@pytest.mark.asyncio
async def test_invalid_response(
    provider,
    validator
):

    payload = {
        "chart": {}
    }

    validator.validate.side_effect = (
        YahooInvalidResponseError(
            "bad payload"
        )
    )

    session = Mock()

    session.get.return_value = MockResponse(
        status=200,
        json_data=payload
    )

    with pytest.raises(
        YahooInvalidResponseError
    ):
        await provider.fetch(
            "AAPL",
            session
        )
        
# --------------------------------------------------
# Timeout Retries
# --------------------------------------------------
@pytest.mark.asyncio
async def test_timeout_retries(
    provider
):

    session = Mock()

    session.get.side_effect = (
        asyncio.TimeoutError()
    )

    with patch(
        "asyncio.sleep",
        new_callable=AsyncMock
    ):

        with pytest.raises(
            asyncio.TimeoutError
        ):
            await provider.fetch(
                "AAPL",
                session
            )

# --------------------------------------------------
# Timeout Retries
# --------------------------------------------------
class MockHttpErrorResponse(
    MockResponse
):

    def raise_for_status(self):

        raise ClientResponseError(
            request_info=Mock(),
            history=(),
            status=500
        )

@pytest.mark.asyncio
async def test_http_error(
    provider
):

    session = Mock()

    session.get.return_value = (
        MockHttpErrorResponse()
    )

    with pytest.raises(
        ClientResponseError
    ):
        await provider.fetch(
            "AAPL",
            session
        )

# --------------------------------------------------
# Logger Verification
# --------------------------------------------------
@pytest.mark.asyncio
async def test_invalid_response_logged(
    provider,
    validator,
    caplog
):

    validator.validate.side_effect = (
        YahooInvalidResponseError(
            "bad payload"
        )
    )

    session = Mock()

    session.get.return_value = MockResponse(
        status=200,
        json_data={}
    )

    with pytest.raises(
        YahooInvalidResponseError
    ):
        await provider.fetch(
            "AAPL",
            session
        )

    assert (
        "Data from Yahoo Finance API is invalid"
        in caplog.text
    )
