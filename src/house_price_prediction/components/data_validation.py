from pathlib import Path
import sys
import pandas as pd

from house_price_prediction.utils.exception import HousePricePredictionException
from house_price_prediction.utils.logger import logger

from house_price_prediction.entity.config_entity import (
    DataValidationConfig,
)


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        self.results=[]
        self.df=None

    # ======================================================
    # File Validation
    # ======================================================

    def validate_file(self,data_path:str) -> bool:
        try:
            path = Path(data_path)
            if not path.exists():
                self.results.append(
                    {
                        "check": "File existence",
                        "status": "FAIL",
                        "message": (
                            f"File not found: {path}"
                        ),
                    }
                )
                return False
            if path.stat().st_size == 0:

                self.results.append(
                    {
                        "check": "File not empty",
                        "status": "FAIL",
                        "message": (
                            f"File is empty: {path}"
                        ),
                    }
                )

                return False

            self.results.append(
                {
                    "check": "File existence",
                    "status": "PASS",
                    "message": (
                        f"File found: {path}"
                    ),
                }
            )

            return True
        except Exception as e:
            raise HousePricePredictionException(e, sys) from e
    # ======================================================
    # Load Dataset
    # ======================================================

    def load_dataset(self,data_path:str) -> None:
        try:
            logger.info(
                f"Loading dataset from: {data_path}"
            )
            self.df = pd.read_csv(data_path,sep='\t')
            logger.info(
                f"Dataset loaded successfully. "
                f"Shape: {self.df.shape}"
            )

        except Exception as e:
            raise HousePricePredictionException(e, sys) from e

    # ======================================================
    # Shape Validation
    # ======================================================

    def validate_shape(self) -> bool:
        try:
            if self.df is None:
                raise ValueError(
                    "Dataset not loaded. "
                    "Call load_dataset() first."
                )
            rows, columns = self.df.shape
            expected_rows = self.config.expected_rows_min
            actual_rows = self.df.shape[0]

            if actual_rows < expected_rows:
                self.results.append(
                    {
                        "check": "Row count",
                        "status": "FAIL",
                        "message": (
                            f"Row count is less than expected. "
                            f"Expected: {expected_rows}, "
                            f"Actual: {actual_rows}"
                        ),
                    }
                )
                return False
            if columns != self.config.expected_columns:
                self.results.append(
                    {
                        "check": "Column count",
                        "status": "FAIL",
                        "message": (
                            f"Column count is not as expected. "
                            f"Expected: {self.config.expected_columns}, "
                            f"Actual: {columns}"
                        ),
                    }
                )
                return False

            self.results.append(
                {
                    "check": "Column count",
                    "status": "PASS",
                    "message": (
                        f"Row count is as expected. "
                        f"Expected: {expected_rows}, "
                        f"Actual: {actual_rows}"
                    ),
                }
            )

            return True
        except Exception as e:
            raise HousePricePredictionException(e, sys) from e

    # ======================================================
    # Required Column Validation
    # ======================================================

    def validate_required_columns(self) -> bool:
        try:
            if self.df is None:
                raise ValueError(
                    "Dataset not loaded. "
                    "Call load_dataset() first."
                )
            missing_columns = [
                col for col in self.config.required_columns
                if col not in self.df.columns
            ]
            if missing_columns:
                self.results.append(
                    {
                        "check": "Required columns",
                        "status": "FAIL",
                        "message": (
                            f"Missing required columns: "
                            f"{', '.join(missing_columns)}"
                        ),
                    }
                )
                return False

            self.results.append(
                {
                    "check": "Required columns",
                    "status": "PASS",
                    "message": (
                        f"All required columns are present."
                    ),
                }
            )

            return True
        except Exception as e:
            raise HousePricePredictionException(e, sys) from e
    # ======================================================
    # Target Validation
    # ======================================================

    def validate_target(self) -> bool:
        try:
            if self.df is None:
                raise ValueError(
                    "Dataset not loaded. "
                    "Call load_dataset() first."
                )
            target_column = self.config.required_columns[0]
            if target_column not in self.df.columns:
                self.results.append(
                    {
                        "check": "Target column existence",
                        "status": "FAIL",
                        "message": (
                            f"Target column '{target_column}' "
                            f"not found in dataset."
                        ),
                    }
                )
                return False
            missing_values = self.df[target_column].isnull().sum()
            if missing_values > 0:
                self.results.append(
                    {
                        "check": "Target column missing values",
                        "status": "FAIL",
                        "message": (
                            f"Target column '{target_column}' "
                            f"contains {missing_values} missing values."
                        ),
                    }
                )
                return False

            self.results.append(
                {
                    "check": "Target column existence",
                    "status": "PASS",
                    "message": (
                        f"Target column '{target_column}' "
                        f"found in dataset."
                    ),
                }
            )

            # Target must be positive for house prices.
            invalid_target_values = (self.df[target_column] <= 0).sum()
            if invalid_target_values > 0:
                self.results.append(
                    {
                        "check": "Target column invalid values",
                        "status": "FAIL",
                        "message": (
                            f"Target column '{target_column}' "
                            f"contains {invalid_target_values} non-positive values."
                        ),
                    }
                )
                return False
            self.results.append(
                {
                    "check": "Target column invalid values",
                    "status": "PASS",
                    "message": (
                        f"All values in target column '{target_column}' "
                        f"are positive."
                    ),
                }
            )
            return True

        except Exception as e:
            raise HousePricePredictionException(e, sys) from e
    # ======================================================
    # Data Quality Validation
    # ======================================================

    def validate_quality(self) -> bool:

        try:

            # ------------------------------------------------
            # Duplicate rows
            # ------------------------------------------------

            duplicate_count = (
                self.df.duplicated().sum()
            )

            if duplicate_count > 0:

                self.results.append(
                    {
                        "check": "Duplicate rows",
                        "status": "WARNING",
                        "message": (
                            f"Found {duplicate_count} "
                            "duplicate rows."
                        ),
                    }
                )

            else:

                self.results.append(
                    {
                        "check": "Duplicate rows",
                        "status": "PASS",
                        "message": (
                            "No duplicate rows found."
                        ),
                    }
                )

            # ------------------------------------------------
            # Missing feature values
            # ------------------------------------------------

            missing_values = (
                self.df.isna().sum().sum()
            )

            if missing_values > 0:

                self.results.append(
                    {
                        "check": "Missing feature values",
                        "status": "WARNING",
                        "message": (
                            f"Found {missing_values} "
                            "missing values."
                        ),
                    }
                )

            else:

                self.results.append(
                    {
                        "check": "Missing feature values",
                        "status": "PASS",
                        "message": (
                            "No missing values found."
                        ),
                    }
                )

            return True

        except Exception as e:

            raise HousePricePredictionException(
                e,
                sys,
            ) from e

    # ======================================================
    # Save Validation Report
    # ======================================================

    def save_validation_report(self) -> None:

        try:

            status_file = Path(
                self.config.status_file
            )

            status_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            lines = []

            lines.append(
                "=" * 60
            )

            lines.append(
                "DATA VALIDATION REPORT"
            )

            lines.append(
                "=" * 60
            )

            lines.append("")

            for result in self.results:

                lines.append(
                    f"[{result['status']}] "
                    f"{result['check']}"
                )

                lines.append(
                    f"    {result['message']}"
                )

                lines.append("")

            has_failure = any(
                result["status"] == "FAIL"
                for result in self.results
            )

            has_warning = any(
                result["status"] == "WARNING"
                for result in self.results
            )

            if has_failure:

                overall_status = "FAIL"

            elif has_warning:

                overall_status = "PASS WITH WARNINGS"

            else:

                overall_status = "PASS"

            lines.append(
                "=" * 60
            )

            lines.append(
                f"OVERALL STATUS: {overall_status}"
            )

            lines.append(
                "=" * 60
            )

            status_file.write_text(
                "\n".join(lines),
                encoding="utf-8",
            )

            logger.info(
                f"Validation report saved to: "
                f"{status_file}"
            )

        except Exception as e:

            raise HousePricePredictionException(
                e,
                sys,
            ) from e

    # ======================================================
    # Run All Validations
    # ======================================================

    def validate_all(
        self,
        data_path: str,
    ) -> bool:

        try:

            logger.info(
                "Starting data validation."
            )

            file_valid = self.validate_file(
                data_path
            )

            if not file_valid:

                self.save_validation_report()

                return False

            self.load_dataset(
                data_path
            )

            shape_valid = (
                self.validate_shape()
            )

            required_columns_valid = (
                self.validate_required_columns()
            )

            if required_columns_valid:

                self.validate_target()

            self.validate_quality()

            self.save_validation_report()

            has_failure = any(
                result["status"] == "FAIL"
                for result in self.results
            )

            if has_failure:

                logger.error(
                    "Data validation failed."
                )

                return False

            logger.info(
                "Data validation completed successfully."
            )

            return True

        except Exception as e:

            raise HousePricePredictionException(
                e,
                sys,
            ) from e