import pandas as pd

from src.data_quality_toolkit.validator import (
    find_missing_columns,
    find_missing_values,
)


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

def test_find_missing_values_returns_rows_with_missing_data():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob", None],
            "email": ["alice@example.com", None, "charlie@example.com"],
        }
    )

    required_columns = ["name", "email"]

    result = find_missing_values(data, required_columns)

    assert result == {
        "name": [2],
        "email": [1],
    }


def test_find_missing_values_returns_empty_dict_when_complete():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "email": ["alice@example.com", "bob@example.com"],
        }
    )

    required_columns = ["name", "email"]

    result = find_missing_values(data, required_columns)

    assert result == {}