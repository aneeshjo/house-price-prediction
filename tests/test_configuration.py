from house_price_prediction.config.configuration import (
    ConfigurationManager,
)


def test_configuration_manager():

    config_manager = ConfigurationManager()

    config = (
        config_manager.get_data_ingestion_config()
    )

    assert config.root_dir == (
        "artifacts/data_ingestion"
    )

    assert config.source_file == (
        "dataset/AmesHousing.txt"
    )

    assert config.local_data_file == (
        "artifacts/data_ingestion/AmesHousing.txt"
    )

def test_data_validation_config():

    config_manager = ConfigurationManager()

    config = (
        config_manager.get_data_validation_config()
    )

    assert config.root_dir == (
        "artifacts/data_validation"
    )

    assert config.status_file == (
        "artifacts/data_validation/status.txt"
    )

    assert config.expected_columns == 82

    assert config.expected_rows_min == 1

    assert "SalePrice" in config.required_columns