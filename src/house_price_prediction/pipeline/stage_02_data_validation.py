import sys

from house_price_prediction.components.data_validation import (
    DataValidation,
)

from house_price_prediction.config.configuration import (
    ConfigurationManager,
)

from house_price_prediction.utils.exception import (
    HousePricePredictionException,
)

from house_price_prediction.utils.logger import logger


def run_data_validation():

    try:

        logger.info(
            "========== Stage 02: Data Validation =========="
        )

        config_manager = ConfigurationManager()

        validation_config = (
            config_manager.get_data_validation_config()
        )

        ingestion_config = (
            config_manager.get_data_ingestion_config()
        )

        data_validation = DataValidation(
            config=validation_config
        )

        status = data_validation.validate_all(
            data_path=ingestion_config.local_data_file
        )

        if status:

            logger.info(
                "Stage 02 completed successfully."
            )

        else:

            logger.error(
                "Stage 02 failed validation."
            )

        return status

    except Exception as e:

        raise HousePricePredictionException(
            e,
            sys,
        ) from e


if __name__ == "__main__":
    run_data_validation()