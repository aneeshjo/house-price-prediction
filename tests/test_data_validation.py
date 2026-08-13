from pathlib import Path

from house_price_prediction.components.data_validation import (
    DataValidation,
)

from house_price_prediction.config.configuration import (
    ConfigurationManager,
)


def test_data_validation():

    config_manager = ConfigurationManager()

    validation_config = (
        config_manager.get_data_validation_config()
    )

    ingestion_config = (
        config_manager.get_data_ingestion_config()
    )

    validator = DataValidation(
        config=validation_config
    )

    status = validator.validate_all(
        data_path=ingestion_config.local_data_file
    )

    assert isinstance(status, bool)

    assert Path(
        validation_config.status_file
    ).exists()