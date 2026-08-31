import sys

from house_price_prediction.components.data_ingestion import (
    DataIngestion
)

from house_price_prediction.components.data_validation import (
    DataValidation
)

from house_price_prediction.components.data_transformation import (
    DataTransformation
)

from house_price_prediction.components.model_trainer import (
    ModelTrainer
)

from house_price_prediction.utils.exception import (
    HousePricePredictionException
)

from house_price_prediction.utils.logger import logger


class TrainingPipeline:

    def __init__(
        self,
        ingestion_config,
        validation_config,
        transformation_config,
        trainer_config
    ):

        self.ingestion_config = ingestion_config
        self.validation_config = validation_config
        self.transformation_config = (
            transformation_config
        )
        self.trainer_config = trainer_config

    def run_pipeline(self):

        try:

            logger.info(
                "========== TRAINING PIPELINE STARTED =========="
            )

            # ---------------------------------------------
            # DATA INGESTION
            # ---------------------------------------------

            logger.info(
                "Step 1: Data Ingestion"
            )

            ingestion = DataIngestion(
                self.ingestion_config
            )

            train_path, test_path = (
                ingestion.initiate_data_ingestion()
            )

            # ---------------------------------------------
            # DATA VALIDATION
            # ---------------------------------------------

            logger.info(
                "Step 2: Data Validation"
            )

            validation = DataValidation(
                self.validation_config
            )

            train_valid = validation.validate_all(
                train_path
            )

            if not train_valid:

                raise ValueError(
                    "Training data validation failed."
                )

            # ---------------------------------------------
            # DATA TRANSFORMATION
            # ---------------------------------------------

            logger.info(
                "Step 3: Data Transformation"
            )

            transformation = DataTransformation(
                self.transformation_config
            )

            train_array, test_array, preprocessor_path = (
                transformation.initiate_data_transformation(
                    train_path,
                    test_path
                )
            )

            # ---------------------------------------------
            # MODEL TRAINING
            # ---------------------------------------------

            logger.info(
                "Step 4: Model Training"
            )

            trainer = ModelTrainer(
                self.trainer_config
            )

            best_model_name, best_result = (
                trainer.initiate_model_training(
                    train_array,
                    test_array
                )
            )

            logger.info(
                "========== TRAINING PIPELINE COMPLETED =========="
            )

            return (
                best_model_name,
                best_result,
                preprocessor_path
            )

        except Exception as e:

            logger.error(
                "Training pipeline failed."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e