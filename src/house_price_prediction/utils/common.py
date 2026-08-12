from pathlib import Path

import yaml


def read_yaml(path_to_yaml: Path) -> dict:

    with open(path_to_yaml, encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file)

    return content if content is not None else {}


def create_directories(path_to_directories: list[Path]) -> None:

    for path in path_to_directories:
        path.mkdir(
            parents=True,
            exist_ok=True
        )