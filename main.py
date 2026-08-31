from house_price_prediction.pipeline.training_pipeline import (
    TrainingPipeline
)

from house_price_prediction.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)


def main():

    ingestion_config = (
        DataIngestionConfig()
    )

    validation_config = (
        DataValidationConfig()
    )

    transformation_config = (
        DataTransformationConfig()
    )

    trainer_config = (
        ModelTrainerConfig()
    )

    pipeline = TrainingPipeline(
        ingestion_config,
        validation_config,
        transformation_config,
        trainer_config
    )

    best_model_name, best_result, _ = (
        pipeline.run_pipeline()
    )

    print(
        "\nTraining completed."
    )

    print(
        f"Best Model: {best_model_name}"
    )

    print(
        f"MAE: {best_result['mae']:.2f}"
    )

    print(
        f"RMSE: {best_result['rmse']:.2f}"
    )

    print(
        f"R²: {best_result['r2']:.4f}"
    )


if __name__ == "__main__":
    main()