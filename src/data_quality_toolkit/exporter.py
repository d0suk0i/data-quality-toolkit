from pathlib import Path

import pandas as pd

from src.data_quality_toolkit.validator import ValidationResult


REPORT_COLUMNS = [
    "issue_type",
    "column",
    "row",
    "details",
]


def build_report_records(
    result: ValidationResult,
) -> list[dict]:
    """
    Convert validation issues into structured report records.

    Args:
        result: Validation result containing detected issues.

    Returns:
        A list of dictionaries representing individual issues.
    """
    records = []

    for column in result.missing_columns:
        records.append(
            {
                "issue_type": "missing_column",
                "column": column,
                "row": None,
                "details": "Required column is missing.",
            }
        )

    for column in result.unexpected_columns:
        records.append(
            {
                "issue_type": "unexpected_column",
                "column": column,
                "row": None,
                "details": "Column is not part of the expected schema.",
            }
        )

    for column, rows in result.missing_values.items():
        for row in rows:
            records.append(
                {
                    "issue_type": "missing_value",
                    "column": column,
                    "row": row,
                    "details": "Required value is missing.",
                }
            )

    for row in result.duplicate_rows:
        records.append(
            {
                "issue_type": "duplicate_row",
                "column": None,
                "row": row,
                "details": "Duplicate record detected.",
            }
        )

    for column, rows in result.invalid_values.items():
        for row in rows:
            records.append(
                {
                    "issue_type": "invalid_value",
                    "column": column,
                    "row": row,
                    "details": "Value is not permitted by the validation rules.",
                }
            )

    return records


def export_report_csv(
    result: ValidationResult,
    output_path: str | Path,
) -> None:
    """
    Export validation issues to a CSV report.

    Args:
        result: Validation result containing detected issues.
        output_path: Destination CSV file.
    """
    path = Path(output_path)

    records = build_report_records(result)

    report = pd.DataFrame(
        records,
        columns=REPORT_COLUMNS,
    )

    report.to_csv(
        path,
        index=False,
    )