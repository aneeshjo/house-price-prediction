from house_price_prediction.components.data_ingestion import (
    DataIngestion,
)
from house_price_prediction.config.configuration import (
    ConfigurationManager,
)
from house_price_prediction.utils.logger import logger


def run_data_ingestion():

    try:

        logger.info(
            "========== Stage 01: Data Ingestion =========="
        )

        config_manager = ConfigurationManager()

        data_ingestion_config = (
            config_manager.get_data_ingestion_config()
        )

        data_ingestion = DataIngestion(
            config=data_ingestion_config
        )

        output_path = (
            data_ingestion.copy_raw_data()
        )

        logger.info(
            f"Data ingestion completed: {output_path}"
        )

    except Exception:
        raise


if __name__ == "__main__":
    run_data_ingestion()