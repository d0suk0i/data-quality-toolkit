from pathlib import Path

import pandas as pd

from src.data_quality_toolkit.validator import ValidationResult
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from src.data_quality_toolkit.utils import source_row_number


REPORT_COLUMNS = [
    "issue_type",
    "column",
    "source_row",
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
                "source_row": None,
                "details": "Required column is missing.",
            }
        )

    for column in result.unexpected_columns:
        records.append(
            {
                "issue_type": "unexpected_column",
                "column": column,
                "source_row": None,
                "details": "Column is not part of the expected schema.",
            }
        )

    for column, rows in result.missing_values.items():
        for row in rows:
            records.append(
                {
                    "issue_type": "missing_value",
                    "column": column,
                    "source_row": source_row_number(row),
                    "details": "Required value is missing.",
                }
            )

    for row in result.duplicate_rows:
        records.append(
            {
                "issue_type": "duplicate_row",
                "column": None,
                "source_row": source_row_number(row),
                "details": "Duplicate record detected.",
            }
        )

    for column, rows in result.invalid_values.items():
        for row in rows:
            records.append(
                {
                    "issue_type": "invalid_value",
                    "column": column,
                    "source_row": source_row_number(row),
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

def export_report_excel(
    result: ValidationResult,
    output_path: str | Path,
) -> None:
    """
    Export validation results to a formatted Excel workbook.

    The workbook contains:
        - Summary sheet with validation status and issue counts.
        - Issues sheet with individual validation problems.

    Args:
        result: Validation result containing detected issues.
        output_path: Destination Excel file.
    """
    path = Path(output_path)

    records = build_report_records(result)

    issues_df = pd.DataFrame(
        records,
        columns=REPORT_COLUMNS,
    )

    issue_counts = {
        "Missing columns": len(result.missing_columns),
        "Unexpected columns": len(result.unexpected_columns),
        "Missing values": sum(
            len(rows)
            for rows in result.missing_values.values()
        ),
        "Duplicate rows": len(result.duplicate_rows),
        "Invalid values": sum(
            len(rows)
            for rows in result.invalid_values.values()
        ),
    }

    summary_rows = [
        {
            "metric": "Validation Status",
            "value": "PASSED" if result.is_valid else "FAILED",
        },
        {
            "metric": "Total Issues",
            "value": len(records),
        },
    ]

    for issue_name, count in issue_counts.items():
        summary_rows.append(
            {
                "metric": issue_name,
                "value": count,
            }
        )

    summary_df = pd.DataFrame(summary_rows)

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:
        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
            header=False,
        )

        issues_df.to_excel(
            writer,
            sheet_name="Issues",
            index=False,
        )

        workbook = writer.book

        summary_sheet = workbook["Summary"]
        issues_sheet = workbook["Issues"]

        for cell in summary_sheet["A"]:
            cell.font = Font(bold=True)

        summary_sheet.column_dimensions["A"].width = 24
        summary_sheet.column_dimensions["B"].width = 16

        for cell in issues_sheet[1]:
            cell.font = Font(bold=True)

        issues_sheet.freeze_panes = "A2"
        issues_sheet.auto_filter.ref = issues_sheet.dimensions

        for column_cells in issues_sheet.columns:
            max_length = 0

            for cell in column_cells:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value)),
                    )

            column_letter = get_column_letter(
                column_cells[0].column
            )

            issues_sheet.column_dimensions[
                column_letter
            ].width = min(max_length + 2, 50)