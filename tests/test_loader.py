import pandas as pd
import pytest

from src.data_quality_toolkit.loader import load_data_file


def test_load_csv(tmp_path):
    original_data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
        }
    )

    file_path = tmp_path / "sample.csv"
    original_data.to_csv(file_path, index=False)

    loaded_data = load_data_file(file_path)

    pd.testing.assert_frame_equal(loaded_data, original_data)


def test_load_xlsx(tmp_path):
    original_data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
        }
    )

    file_path = tmp_path / "sample.xlsx"
    original_data.to_excel(file_path, index=False)

    loaded_data = load_data_file(file_path)

    pd.testing.assert_frame_equal(loaded_data, original_data)


def test_missing_file_raises_error(tmp_path):
    file_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_data_file(file_path)


def test_unsupported_file_type_raises_error(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("some data")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_data_file(file_path)