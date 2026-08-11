from pathlib import Path
import yaml

from house_price_prediction.entity.config_entity import DataIngestionConfig


class ConfigurationManager:

    def __init__(
        self,
        config_file_path="config/config.yaml",
        params_file_path="config/params.yaml",
        schema_file_path="config/schema.yaml"
    ):
        with open(config_file_path) as config_file:
            self.config = yaml.safe_load(config_file)

        with open(params_file_path) as params_file:
            self.params = yaml.safe_load(params_file)

        with open(schema_file_path) as schema_file:
            self.schema = yaml.safe_load(schema_file)

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config["data_ingestion"]

        return DataIngestionConfig(
            root_dir=config["root_dir"],
            source_file=config["source_file"],
            local_data_file=config["local_data_file"]
        )