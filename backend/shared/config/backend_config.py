from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s |%(levelname)-8s |%(name)s |%(message)s"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
