import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "running_logs.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s "
           "%(name)s - %(message)s",
)


logger = logging.getLogger("house_price_prediction")