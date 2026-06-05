import asyncio

from pipelines.historical_ingestion.config import SYMBOLS
from pipelines.historical_ingestion.pipeline import HisotricalIngestion

async def main():
    await HisotricalIngestion(SYMBOLS).run_pipeline()

if __name__ == '__main__':
    asyncio.run(main())