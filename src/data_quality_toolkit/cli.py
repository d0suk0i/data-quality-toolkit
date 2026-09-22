import argparse

from src.data_quality_toolkit.loader import load_data_file
from src.data_quality_toolkit.report import format_validation_report
from src.data_quality_toolkit.validator import validate_data
from src.data_quality_toolkit.config import load_validation_config
from src.data_quality_toolkit.exporter import (
    export_report_csv,
    export_report_excel,
)
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """
    Create the command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Validate CSV and Excel data files."
    )

    parser.add_argument(
        "file",
        help="Path to the CSV or XLSX file to validate.",
    )

    parser.add_argument(
        "--required",
        nargs="+",
        default=[],
        help="Columns that must exist and contain values.",
    )

    parser.add_argument(
        "--expected",
        nargs="+",
        help="Complete list of columns expected in the file.",
    )

    parser.add_argument(
        "--duplicate-key",
        nargs="+",
        help="Columns used to identify duplicate rows.",
    )

    parser.add_argument(
        "--config",
        help="Path to a YAML validation configuration file.",

    )

    parser.add_argument(
        "--output",
        help="Optional path for exporting the validation report as CSV.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run the data quality validator from the command line.

    Returns:
        0 when validation passes.
        1 when validation fails.
        2 when the command cannot complete because of an input
        or configuration error.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        data = load_data_file(args.file)

        config = {}

        if args.config:
            config = load_validation_config(args.config)

        required_columns = config.get(
            "required_columns",
            args.required,
        )

        expected_columns = config.get(
            "expected_columns",
            args.expected,
        )

        if expected_columns is None:
            expected_columns = list(data.columns)

        duplicate_subset = config.get(
            "duplicate_subset",
            args.duplicate_key,
        )

        allowed_values = config.get(
            "allowed_values",
        )

        result = validate_data(
            data=data,
            expected_columns=expected_columns,
            required_columns=required_columns,
            allowed_values=allowed_values,
            duplicate_subset=duplicate_subset,
        )

        print(format_validation_report(result))

        if args.output:
            output_path = Path(args.output)
            extension = output_path.suffix.lower()

            if extension == ".csv":
                export_report_csv(
                    result=result,
                    output_path=output_path,
                )

            elif extension == ".xlsx":
                export_report_excel(
                    result=result,
                    output_path=output_path,
                )

            else:
                print(
                    "Error: Output file must use "
                    ".csv or .xlsx extension."
                )
                return 2

            print(f"Report saved to: {output_path}")

        return 0 if result.is_valid else 1

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())