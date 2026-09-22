from data_quality_toolkit.report import format_validation_report
from data_quality_toolkit.validator import ValidationResult


def test_format_validation_report_for_valid_data():
    result = ValidationResult()

    report = format_validation_report(result)

    assert report == "Validation passed: no issues found."


def test_format_validation_report_lists_errors():
    result = ValidationResult(
        missing_columns=["email"],
        unexpected_columns=["notes"],
        missing_values={
            "name": [2],
        },
        duplicate_rows=[4],
        invalid_values={
            "employment_type": [1, 3],
        },
    )

    report = format_validation_report(result)

    assert "Missing columns: email" in report
    assert "Unexpected columns: notes" in report
    assert "Missing values in 'name': rows 4" in report
    assert "Duplicate rows: 6" in report
    assert "Invalid values in 'employment_type': rows 3, 5" in report