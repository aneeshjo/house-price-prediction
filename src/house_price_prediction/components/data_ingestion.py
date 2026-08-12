from pathlib import Path
import shutil

from house_price_prediction.entity.config_entity import (
    DataIngestionConfig,
)
from house_price_prediction.utils.exception import (
    HousePricePredictionException,
)
from house_price_prediction.utils.logger import logger


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_raw_data(self) -> str:

        try:

            source_file = Path(
                self.config.source_file
            )

            destination_file = Path(
                self.config.local_data_file
            )

            logger.info(
                "Starting data ingestion."
            )

            logger.info(
                f"Source file: {source_file}"
            )

            logger.info(
                f"Destination file: {destination_file}"
            )

            if not source_file.exists():

                raise FileNotFoundError(
                    f"Source dataset not found: "
                    f"{source_file}"
                )

            destination_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_file,
                destination_file,
            )

            logger.info(
                "Raw dataset copied successfully."
            )

            return str(destination_file)

        except Exception as e:

            raise HousePricePredictionException(
                e,
                __import__("sys"),
            ) from e