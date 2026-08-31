import os
import sys

import joblib
import numpy as np

from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from house_price_prediction.utils.exception import (
    HousePricePredictionException
)
from house_price_prediction.utils.logger import logger


class ModelTrainer:

    def __init__(self, config):
        self.config = config

    def evaluate_model(
        self,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        try:

            models = {

                "Ridge": Ridge(
                    alpha=1.0
                ),

                "Random Forest": RandomForestRegressor(
                    n_estimators=300,
                    random_state=42,
                    n_jobs=-1
                ),

                "Gradient Boosting": GradientBoostingRegressor(
                    n_estimators=300,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=42
                )
            }

            results = []

            trained_models = {}

            for name, model in models.items():

                logger.info(
                    f"Training model: {name}"
                )

                model.fit(
                    X_train,
                    y_train
                )

                predictions = model.predict(
                    X_test
                )

                mae = mean_absolute_error(
                    y_test,
                    predictions
                )

                rmse = np.sqrt(
                    mean_squared_error(
                        y_test,
                        predictions
                    )
                )

                r2 = r2_score(
                    y_test,
                    predictions
                )

                results.append(
                    {
                        "model": name,
                        "mae": mae,
                        "rmse": rmse,
                        "r2": r2
                    }
                )

                trained_models[name] = model

                logger.info(
                    f"{name} | "
                    f"MAE={mae:.2f} | "
                    f"RMSE={rmse:.2f} | "
                    f"R2={r2:.4f}"
                )

            return (
                results,
                trained_models
            )

        except Exception as e:

            logger.error(
                "Error while evaluating models."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e

    def initiate_model_training(
        self,
        train_array,
        test_array
    ):

        try:

            logger.info(
                "Starting model training."
            )

            X_train = train_array[:, :-1]
            y_train = train_array[:, -1]

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            results, trained_models = (
                self.evaluate_model(
                    X_train,
                    y_train,
                    X_test,
                    y_test
                )
            )

            best_result = max(
                results,
                key=lambda x: x["r2"]
            )

            best_model_name = (
                best_result["model"]
            )

            best_model = (
                trained_models[
                    best_model_name
                ]
            )

            logger.info(
                f"Best model: "
                f"{best_model_name}"
            )

            logger.info(
                f"Best model R2: "
                f"{best_result['r2']:.4f}"
            )

            if best_result["r2"] < 0.70:

                raise ValueError(
                    "No acceptable model found. "
                    f"Best R2: {best_result['r2']:.4f}"
                )

            os.makedirs(
                os.path.dirname(
                    self.config.model_path
                ),
                exist_ok=True
            )

            joblib.dump(
                best_model,
                self.config.model_path
            )

            logger.info(
                f"Best model saved at: "
                f"{self.config.model_path}"
            )

            return best_model_name, best_result

        except Exception as e:

            logger.error(
                "Error occurred during model training."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e