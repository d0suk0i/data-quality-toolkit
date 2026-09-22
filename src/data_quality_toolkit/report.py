from data_quality_toolkit.validator import ValidationResult
from data_quality_toolkit.utils import source_row_number


def format_validation_report(result: ValidationResult) -> str:
    """
    Convert a ValidationResult into a readable text report.

    Args:
        result: Validation result containing detected data issues.

    Returns:
        A human-readable validation report.
    """
    if result.is_valid:
        return "Validation passed: no issues found."

    lines = ["Validation failed:"]

    if result.missing_columns:
        columns = ", ".join(result.missing_columns)
        lines.append(f"Missing columns: {columns}")

    if result.unexpected_columns:
        columns = ", ".join(result.unexpected_columns)
        lines.append(f"Unexpected columns: {columns}")

    for column, rows in result.missing_values.items():
        row_text = ", ".join(
            str(source_row_number(row))
            for row in rows
        )

        lines.append(
            f"Missing values in '{column}': rows {row_text}"
        )

    if result.duplicate_rows:
        row_text = ", ".join(
            str(source_row_number(row))
            for row in result.duplicate_rows
        )
        lines.append(f"Duplicate rows: {row_text}")

    for column, rows in result.invalid_values.items():
        row_text = ", ".join(
            str(source_row_number(row))
            for row in rows
        )

        lines.append(
            f"Invalid values in '{column}': rows {row_text}"
        )

    return "\n".join(lines)