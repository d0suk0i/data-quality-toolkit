from pathlib import Path

import yaml


LIST_CONFIG_KEYS = (
    "required_columns",
    "expected_columns",
    "duplicate_subset",
)


def load_validation_config(file_path: str | Path) -> dict:
    """
    Load and validate rules from a YAML configuration file.

    Args:
        file_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing validated configuration settings.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration structure is invalid.
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

    for key in LIST_CONFIG_KEYS:
        value = config.get(key)

        if value is not None and not isinstance(value, list):
            raise ValueError(
                f"{key} must be a list."
            )

    allowed_values = config.get("allowed_values")

    if allowed_values is not None:
        if not isinstance(allowed_values, dict):
            raise ValueError(
                "allowed_values must be a mapping."
            )

        for column, values in allowed_values.items():
            if not isinstance(values, list):
                raise ValueError(
                    f"Allowed values for '{column}' must be a list."
                )

    return config