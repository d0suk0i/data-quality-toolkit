import pytest

from data_quality_toolkit.config import load_validation_config


def test_load_validation_config(tmp_path):
    config_file = tmp_path / "rules.yaml"

    config_file.write_text(
        """
required_columns:
  - id
  - name

expected_columns:
  - id
  - name
  - email

duplicate_subset:
  - id

allowed_values:
  status:
    - active
    - inactive
""",
        encoding="utf-8",
    )

    config = load_validation_config(config_file)

    assert config["required_columns"] == ["id", "name"]
    assert config["expected_columns"] == ["id", "name", "email"]
    assert config["duplicate_subset"] == ["id"]
    assert config["allowed_values"] == {
        "status": ["active", "inactive"]
    }


def test_missing_config_file_raises_error(tmp_path):
    config_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_validation_config(config_file)


def test_invalid_config_root_raises_error(tmp_path):
    config_file = tmp_path / "invalid.yaml"

    config_file.write_text(
        """
- item1
- item2
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="configuration must be a mapping"):
        load_validation_config(config_file)

def test_config_rejects_non_list_required_columns(tmp_path):
    config_file = tmp_path / "rules.yaml"

    config_file.write_text(
        """
required_columns: name
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="required_columns must be a list",
    ):
        load_validation_config(config_file)


def test_config_rejects_non_mapping_allowed_values(tmp_path):
    config_file = tmp_path / "rules.yaml"

    config_file.write_text(
        """
allowed_values:
  - full-time
  - part-time
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="allowed_values must be a mapping",
    ):
        load_validation_config(config_file)


def test_config_rejects_invalid_allowed_value_list(tmp_path):
    config_file = tmp_path / "rules.yaml"

    config_file.write_text(
        """
allowed_values:
  employment_type: full-time
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Allowed values for 'employment_type' must be a list",
    ):
        load_validation_config(config_file)