import os
import sys

import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from house_price_prediction.utils.exception import (
    HousePricePredictionException
)
from house_price_prediction.utils.logger import logger


class DataTransformation:

    def __init__(self, config):
        self.config = config

    # =========================================================
    # Create Preprocessing Object
    # =========================================================

    def get_data_transformer_object(
        self,
        numerical_columns,
        categorical_columns
    ):

        try:

            logger.info(
                "Creating data transformation pipelines."
            )

            # -------------------------------------------------
            # Numerical Pipeline
            # -------------------------------------------------

            numerical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="median"
                        )
                    )
                ]
            )

            logger.info(
                "Numerical pipeline created."
            )

            # -------------------------------------------------
            # Categorical Pipeline
            # -------------------------------------------------

            categorical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="most_frequent"
                        )
                    ),
                    (
                        "encoder",
                        OneHotEncoder(
                            handle_unknown="ignore"
                        )
                    )
                ]
            )

            logger.info(
                "Categorical pipeline created."
            )

            # -------------------------------------------------
            # Column Transformer
            # -------------------------------------------------

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "num",
                        numerical_pipeline,
                        numerical_columns
                    ),
                    (
                        "cat",
                        categorical_pipeline,
                        categorical_columns
                    )
                ],
                remainder="drop"
            )

            logger.info(
                "ColumnTransformer created successfully."
            )

            return preprocessor

        except Exception as e:

            logger.error(
                "Error occurred while creating "
                "data transformation object."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e

    # =========================================================
    # Initiate Data Transformation
    # =========================================================

    def initiate_data_transformation(
        self,
        train_path,
        test_path
    ):

        try:

            logger.info(
                "Starting data transformation."
            )

            # -------------------------------------------------
            # Read Train and Test Data
            # -------------------------------------------------

            train_df = pd.read_csv(
                train_path
            )

            test_df = pd.read_csv(
                test_path
            )

            logger.info(
                f"Train dataset loaded. "
                f"Shape: {train_df.shape}"
            )

            logger.info(
                f"Test dataset loaded. "
                f"Shape: {test_df.shape}"
            )

            # -------------------------------------------------
            # Separate Features and Target
            # -------------------------------------------------

            target_column = "SalePrice"

            X_train = train_df.drop(
                columns=[target_column]
            )

            y_train = train_df[
                target_column
            ]

            X_test = test_df.drop(
                columns=[target_column]
            )

            y_test = test_df[
                target_column
            ]

            logger.info(
                "Features and target separated successfully."
            )

            # -------------------------------------------------
            # Identify Numerical and Categorical Columns
            # -------------------------------------------------

            numerical_columns = (
                X_train
                .select_dtypes(
                    include=["int64", "float64"]
                )
                .columns
                .tolist()
            )

            categorical_columns = (
                X_train
                .select_dtypes(
                    include=["object"]
                )
                .columns
                .tolist()
            )

            logger.info(
                f"Numerical columns: "
                f"{len(numerical_columns)}"
            )

            logger.info(
                f"Categorical columns: "
                f"{len(categorical_columns)}"
            )

            # -------------------------------------------------
            # Create Preprocessor
            # -------------------------------------------------

            preprocessor = (
                self.get_data_transformer_object(
                    numerical_columns,
                    categorical_columns
                )
            )

            logger.info(
                "Fitting preprocessor on training data."
            )

            # -------------------------------------------------
            # Fit ONLY on Training Data
            # -------------------------------------------------

            X_train_transformed = (
                preprocessor.fit_transform(
                    X_train
                )
            )

            logger.info(
                "Training data transformation completed."
            )

            # -------------------------------------------------
            # Transform Test Data
            # -------------------------------------------------

            logger.info(
                "Transforming test data."
            )

            X_test_transformed = (
                preprocessor.transform(
                    X_test
                )
            )

            logger.info(
                "Test data transformation completed."
            )

            # -------------------------------------------------
            # Save Preprocessor
            # -------------------------------------------------

            preprocessor_path = (
                self.config.preprocessor_path
            )

            os.makedirs(
                os.path.dirname(preprocessor_path),
                exist_ok=True
            )

            joblib.dump(
                preprocessor,
                preprocessor_path
            )

            logger.info(
                f"Preprocessor saved to: "
                f"{preprocessor_path}"
            )

            # -------------------------------------------------
            # Combine X and y
            # -------------------------------------------------

            import numpy as np

            train_arr = np.c_[
                X_train_transformed,
                y_train.to_numpy()
            ]

            test_arr = np.c_[
                X_test_transformed,
                y_test.to_numpy()
            ]

            logger.info(
                f"Transformed train array shape: "
                f"{train_arr.shape}"
            )

            logger.info(
                f"Transformed test array shape: "
                f"{test_arr.shape}"
            )

            logger.info(
                "Data transformation completed successfully."
            )

            return (
                train_arr,
                test_arr,
                preprocessor
            )

        except Exception as e:

            logger.error(
                "Error occurred during data transformation."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e