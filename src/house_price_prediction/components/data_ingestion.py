import shutil
from pathlib import Path

from house_price_prediction.entity.config_entity import DataIngestionConfig


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_raw_data(self) -> str:

        source_file = Path(self.config.source_file)
        destination_file = Path(self.config.local_data_file)

        if not source_file.exists():
            raise FileNotFoundError(
                f"Source dataset not found: {source_file}"
            )

        destination_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            source_file,
            destination_file
        )

        return str(destination_file)