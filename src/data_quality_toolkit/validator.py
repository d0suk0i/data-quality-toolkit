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