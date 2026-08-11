import yaml
from pathlib import Path


def read_yaml_file(file_path: Path) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    Args:
        file_path (Path): The path to the YAML file.
    """
    with open(file_path, 'rb') as yaml_file:
        return yaml.safe_load(yaml_file)