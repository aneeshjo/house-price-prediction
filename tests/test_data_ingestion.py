from pathlib import Path

from house_price_prediction.components.data_ingestion import (
    DataIngestion,
)
from house_price_prediction.config.configuration import (
    ConfigurationManager,
)


def test_data_ingestion():

    config_manager = ConfigurationManager()

    config = (
        config_manager.get_data_ingestion_config()
    )

    ingestion = DataIngestion(
        config=config
    )

    output_path = ingestion.copy_raw_data()

    assert Path(output_path).exists()