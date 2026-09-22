import pandas as pd

from src.data_quality_toolkit.validator import find_missing_columns


def test_find_missing_columns_returns_missing_columns():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
        }
    )

    required_columns = ["name", "age", "email"]

    result = find_missing_columns(data, required_columns)

    assert result == ["email"]


def test_find_missing_columns_returns_empty_list_when_all_exist():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
        }
    )

    required_columns = ["name", "age"]

    result = find_missing_columns(data, required_columns)

    assert result == []