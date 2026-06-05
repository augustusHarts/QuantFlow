from aiohttp import ClientTimeout
from pathlib import Path

RAW_DIR = Path('datasets/raw')
RAW_DIR.mkdir(parents=True,exist_ok=True)

BASE_URL = 'https://query1.finance.yahoo.com/v8/finance/chart'

API_TIMEOUT = ClientTimeout(total=20)
YAHOO_RANGE = '1y'
YAHOO_INTERVAL = '1d'