from aiohttp import ClientTimeout
from typing import Final

BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart'

API_TIMEOUT = ClientTimeout(total=20)

YAHOO_RANGE = '1y'
YAHOO_INTERVAL = '1d'

DEFAULT_HEADERS: Final[dict[str, str]] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )
}