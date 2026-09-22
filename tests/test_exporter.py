import pandas as pd

from src.data_quality_toolkit.exporter import export_report_csv
from src.data_quality_toolkit.validator import ValidationResult


def test_export_report_csv_creates_report(tmp_path):
    result = ValidationResult(
        missing_columns=["email"],
        unexpected_columns=["notes"],
        missing_values={"name": [2]},
        duplicate_rows=[4],
        invalid_values={"employment_type": [1, 3]},
    )

    output_path = tmp_path / "report.csv"

    export_report_csv(result, output_path)

    report = pd.read_csv(output_path)

    assert list(report.columns) == [
        "issue_type",
        "column",
        "row",
        "details",
    ]

    assert len(report) == 6

    assert "missing_column" in report["issue_type"].values
    assert "unexpected_column" in report["issue_type"].values
    assert "missing_value" in report["issue_type"].values
    assert "duplicate_row" in report["issue_type"].values
    assert "invalid_value" in report["issue_type"].values


def test_export_report_csv_handles_valid_result(tmp_path):
    result = ValidationResult()

    output_path = tmp_path / "report.csv"

    export_report_csv(result, output_path)

    report = pd.read_csv(output_path)

    assert len(report) == 0
    assert list(report.columns) == [
        "issue_type",
        "column",
        "row",
        "details",
    ]