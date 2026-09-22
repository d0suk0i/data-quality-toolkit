import pandas as pd


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