import pandas as pd

from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    missing_columns: list[str] = field(default_factory=list)
    unexpected_columns: list[str] = field(default_factory=list)
    missing_values: dict[str, list[int]] = field(default_factory=dict)
    duplicate_rows: list[int] = field(default_factory=list)
    invalid_values: dict[str, list[int]] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return not any(
            [
                self.missing_columns,
                self.unexpected_columns,
                self.missing_values,
                self.duplicate_rows,
                self.invalid_values,
            ]
        )

def find_missing_columns(
    data: pd.DataFrame,
    required_columns: list[str],
) -> list[str]:
    """
    Return required columns that are missing from the DataFrame.

    Args:
        data: DataFrame to validate.
        required_columns: Column names that must exist.

    Returns:
        A list containing any required columns that are missing.
    """
    return [
        column
        for column in required_columns
        if column not in data.columns
    ]

def find_missing_values(
    data: pd.DataFrame,
    required_columns: list[str],
) -> dict[str, list[int]]:
    """
    Find missing values in required columns.

    Args:
        data: DataFrame to validate.
        required_columns: Columns that must contain values.

    Returns:
        A dictionary where each key is a column name and each value
        is a list of row indexes containing missing data.
    """
    missing_values = {}

    for column in required_columns:
        if column not in data.columns:
            continue

        missing_rows = data.index[data[column].isna()].tolist()

        if missing_rows:
            missing_values[column] = missing_rows

    return missing_values

def find_duplicate_rows(
    data: pd.DataFrame,
    subset: list[str] | None = None,
) -> list[int]:
    """
    Find duplicate rows in a DataFrame.

    Args:
        data: DataFrame to validate.
        subset: Optional list of columns used to determine duplicates.

    Returns:
        A list of row indexes that are duplicates of earlier rows.
    """
    duplicate_mask = data.duplicated(
        subset=subset,
        keep="first",
    )

    return data.index[duplicate_mask].tolist()

def find_invalid_values(
    data: pd.DataFrame,
    column: str,
    allowed_values: list,
) -> list[int]:
    """
    Find rows containing values that are not allowed.

    Missing values are ignored because they are handled separately
    by missing-value validation.

    Args:
        data: DataFrame to validate.
        column: Column to check.
        allowed_values: Values permitted in the column.

    Returns:
        A list of row indexes containing invalid values.
    """
    if column not in data.columns:
        return []

    invalid_mask = (
        data[column].notna()
        & ~data[column].isin(allowed_values)
    )

    return data.index[invalid_mask].tolist()

def find_unexpected_columns(
    data: pd.DataFrame,
    expected_columns: list[str],
) -> list[str]:
    """
    Return columns that exist in the DataFrame but are not expected.

    Args:
        data: DataFrame to validate.
        expected_columns: Column names allowed by the schema.

    Returns:
        A list of unexpected column names.
    """
    return [
        column
        for column in data.columns
        if column not in expected_columns
    ]

def validate_data(
    data: pd.DataFrame,
    expected_columns: list[str],
    required_columns: list[str],
    allowed_values: dict[str, list] | None = None,
    duplicate_subset: list[str] | None = None,
) -> ValidationResult:
    """
    Run multiple validation checks against a DataFrame.

    Args:
        data: DataFrame to validate.
        expected_columns: Columns allowed by the schema.
        required_columns: Columns that must exist and contain values.
        allowed_values: Optional mapping of columns to permitted values.
        duplicate_subset: Optional columns used for duplicate detection.

    Returns:
        ValidationResult containing all detected issues.
    """
    invalid_values = {}

    if allowed_values:
        for column, values in allowed_values.items():
            invalid_rows = find_invalid_values(
                data=data,
                column=column,
                allowed_values=values,
            )

            if invalid_rows:
                invalid_values[column] = invalid_rows

    return ValidationResult(
        missing_columns=find_missing_columns(
            data,
            required_columns,
        ),
        unexpected_columns=find_unexpected_columns(
            data,
            expected_columns,
        ),
        missing_values=find_missing_values(
            data,
            required_columns,
        ),
        duplicate_rows=find_duplicate_rows(
            data,
            subset=duplicate_subset,
        ),
        invalid_values=invalid_values,
    )