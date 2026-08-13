from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: str
    source_file: str
    local_data_file: str

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: str
    status_file: str
    expected_columns: int
    expected_rows_min: int
    required_columns: list[str]