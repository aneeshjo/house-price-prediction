import logging
from pathlib import Path
from datetime import datetime


# ==========================================================
# Create Timestamp
# ==========================================================

TIMESTAMP = datetime.now().strftime(
    "%m_%d_%Y_%H_%M_%S"
)


# ==========================================================
# Create Log Directory
# ==========================================================

logs_path = Path("logs") / TIMESTAMP

logs_path.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# Create Log File
# ==========================================================

LOG_FILE_PATH = logs_path / f"running_logs-{TIMESTAMP}.log"


# ==========================================================
# Create Logger
# ==========================================================

logger = logging.getLogger(
    "house_price_prediction"
)

logger.setLevel(logging.INFO)


# ==========================================================
# Create File Handler
# ==========================================================

if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE_PATH,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s "
        "%(name)s - %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)