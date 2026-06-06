from pathlib import Path
from shared.enums.datalayer import DataLayer

DATASET_DIR = Path("datasets")

RAW_DIR = DATASET_DIR / DataLayer.RAW
PROCESSED_DIR = DATASET_DIR / DataLayer.PROCESSED
CURATED_DIR = DATASET_DIR / DataLayer.CURATED

for path in (
    RAW_DIR,
    PROCESSED_DIR,
    CURATED_DIR
):
    path.mkdir(
        parents=True,
        exist_ok=True
    )