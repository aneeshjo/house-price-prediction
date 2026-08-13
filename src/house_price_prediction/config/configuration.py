from house_price_prediction.constants import (
    CONFIG_FILE_PATH,
    PARAMS_FILE_PATH,
    SCHEMA_FILE_PATH,
)

from house_price_prediction.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)

from house_price_prediction.utils.common import read_yaml


class ConfigurationManager:

    def __init__(
        self,
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH,
        schema_file_path=SCHEMA_FILE_PATH,
    ):

        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)

    def get_data_ingestion_config(
        self,
    ) -> DataIngestionConfig:

        config = self.config["data_ingestion"]

        return DataIngestionConfig(
            root_dir=config["root_dir"],
            source_file=config["source_file"],
            local_data_file=config["local_data_file"],
        )

    def get_data_validation_config(
        self,
    ) -> DataValidationConfig:

        config = self.config["data_validation"]
        schema = self.schema["DATA_VALIDATION"]

        return DataValidationConfig(
            root_dir=config["root_dir"],
            status_file=config["status_file"],
            expected_columns=schema["expected_columns"],
            expected_rows_min=schema["expected_rows_min"],
            required_columns=schema["required_columns"],
        )