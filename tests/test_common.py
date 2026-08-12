from pathlib import Path

from house_price_prediction.utils.common import (
    create_directories,
    read_yaml,
)


def test_read_yaml():

    config = read_yaml(
        Path("config/config.yaml")
    )

    assert isinstance(config, dict)
    assert "artifacts_root" in config


def test_create_directories(tmp_path):

    test_directory = tmp_path / "test_directory"

    create_directories([test_directory])

    assert test_directory.exists()
    assert test_directory.is_dir()