from pathlib import Path

import pandas as pd


def load_data_file(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Args:
        file_path: Path to the input file.

    Returns:
        A pandas DataFrame containing the file data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is not supported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    file_extension = path.suffix.lower()

    if file_extension == ".csv":
        return pd.read_csv(path)

    if file_extension == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")

    raise ValueError(
        f"Unsupported file type: {file_extension}. "
        "Supported types are .csv and .xlsx."
    )