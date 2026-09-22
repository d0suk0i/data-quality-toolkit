import argparse

from src.data_quality_toolkit.loader import load_data_file
from src.data_quality_toolkit.report import format_validation_report
from src.data_quality_toolkit.validator import validate_data


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

    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Run the data quality validator from the command line.

    Args:
        argv: Optional list of command-line arguments.

    Returns:
        0 when validation passes.
        1 when validation fails.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    data = load_data_file(args.file)

    expected_columns = (
        args.expected
        if args.expected is not None
        else list(data.columns)
    )

    result = validate_data(
        data=data,
        expected_columns=expected_columns,
        required_columns=args.required,
        duplicate_subset=args.duplicate_key,
    )

    print(format_validation_report(result))

    return 0 if result.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())