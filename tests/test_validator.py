import pandas as pd

from data_quality_toolkit.validator import (
    ValidationResult,
    find_duplicate_rows,
    find_invalid_values,
    find_missing_columns,
    find_missing_values,
    find_unexpected_columns,
    validate_data,
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

def test_find_invalid_values_returns_invalid_rows():
    data = pd.DataFrame(
        {
            "employment_type": [
                "full-time",
                "part-time",
                "temporary",
                "contract",
            ]
        }
    )

    allowed_values = [
        "full-time",
        "part-time",
        "contract",
    ]

    result = find_invalid_values(
        data,
        column="employment_type",
        allowed_values=allowed_values,
    )

    assert result == [2]


def test_find_invalid_values_returns_empty_list_when_valid():
    data = pd.DataFrame(
        {
            "employment_type": [
                "full-time",
                "part-time",
                "contract",
            ]
        }
    )

    allowed_values = [
        "full-time",
        "part-time",
        "contract",
    ]

    result = find_invalid_values(
        data,
        column="employment_type",
        allowed_values=allowed_values,
    )

    assert result == []


def test_find_invalid_values_ignores_missing_values():
    data = pd.DataFrame(
        {
            "employment_type": [
                "full-time",
                None,
                "contract",
            ]
        }
    )

    allowed_values = [
        "full-time",
        "part-time",
        "contract",
    ]

    result = find_invalid_values(
        data,
        column="employment_type",
        allowed_values=allowed_values,
    )

    assert result == []

def test_find_unexpected_columns_returns_extra_columns():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
            "notes": ["A", "B"],
        }
    )

    expected_columns = ["name", "age"]

    result = find_unexpected_columns(data, expected_columns)

    assert result == ["notes"]


def test_find_unexpected_columns_returns_empty_list_when_schema_matches():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "age": [30, 40],
        }
    )

    expected_columns = ["name", "age"]

    result = find_unexpected_columns(data, expected_columns)

    assert result == []

def test_validation_result_is_valid_when_no_errors():
    result = ValidationResult()

    assert result.is_valid is True


def test_validation_result_is_invalid_when_errors_exist():
    result = ValidationResult(
        missing_columns=["email"]
    )

    assert result.is_valid is False


def test_validate_data_combines_validation_results():
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob", None],
            "employment_type": [
                "full-time",
                "temporary",
                "contract",
            ],
            "extra_column": [1, 2, 3],
        }
    )

    result = validate_data(
        data=data,
        expected_columns=[
            "name",
            "employment_type",
            "email",
        ],
        required_columns=[
            "name",
            "employment_type",
            "email",
        ],
        allowed_values={
            "employment_type": [
                "full-time",
                "part-time",
                "contract",
            ]
        },
    )

    assert result.missing_columns == ["email"]
    assert result.unexpected_columns == ["extra_column"]
    assert result.missing_values == {
        "name": [2]
    }
    assert result.invalid_values == {
        "employment_type": [1]
    }
    assert result.is_valid is False