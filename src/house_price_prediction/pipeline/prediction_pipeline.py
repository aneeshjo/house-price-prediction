import sys

import joblib
import pandas as pd

from house_price_prediction.utils.exception import (
    HousePricePredictionException
)
from house_price_prediction.utils.logger import logger


class PredictionPipeline:

    def __init__(
        self,
        model_path,
        preprocessor_path
    ):

        self.model_path = model_path
        self.preprocessor_path = (
            preprocessor_path
        )

    def predict(self, features):

        try:

            logger.info(
                "Starting prediction."
            )

            model = joblib.load(
                self.model_path
            )

            preprocessor = joblib.load(
                self.preprocessor_path
            )

            if isinstance(
                features,
                dict
            ):

                features = pd.DataFrame(
                    [features]
                )

            transformed_features = (
                preprocessor.transform(
                    features
                )
            )

            prediction = model.predict(
                transformed_features
            )

            logger.info(
                "Prediction completed successfully."
            )

            return prediction[0]

        except Exception as e:

            logger.error(
                "Error occurred during prediction."
            )

            raise HousePricePredictionException(
                e,
                sys
            ) from e