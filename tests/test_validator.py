import pandas as pd

from src.data_quality_toolkit.validator import (
    find_missing_columns,
    find_missing_values,
    find_duplicate_rows,
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

def test_find_duplicate_rows_detects_exact_duplicates():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Alice"],
            "email": [
                "alice@example.com",
                "bob@example.com",
                "alice@example.com",
            ],
        }
    )

    result = find_duplicate_rows(data)

    assert result == [2]


def test_find_duplicate_rows_by_column():
    data = pd.DataFrame(
        {
            "id": [101, 102, 101],
            "name": ["Alice", "Bob", "Alice Updated"],
        }
    )

    result = find_duplicate_rows(data, subset=["id"])

    assert result == [2]


def test_find_duplicate_rows_returns_empty_list_when_unique():
    data = pd.DataFrame(
        {
            "id": [101, 102, 103],
            "name": ["Alice", "Bob", "Charlie"],
        }
    )

    result = find_duplicate_rows(data)

    assert result == []