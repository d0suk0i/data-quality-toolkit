from pathlib import Path

import yaml


def load_validation_config(file_path: str | Path) -> dict:
    """
    Load validation rules from a YAML configuration file.

    Args:
        file_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing validation settings.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the YAML root is not a mapping.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as config_file:
        config = yaml.safe_load(config_file)

    if config is None:
        return {}

    if not isinstance(config, dict):
        raise ValueError(
            "Validation configuration must be a mapping."
        )

    return config