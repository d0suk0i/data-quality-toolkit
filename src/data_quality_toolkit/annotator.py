from pathlib import Path
from shutil import copy2

from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from src.data_quality_toolkit.utils import source_row_number
from src.data_quality_toolkit.validator import ValidationResult


# Professional, subdued workbook palette.
MISSING_VALUE_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFFFF2CC",
)

INVALID_VALUE_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFF4CCCC",
)

DUPLICATE_ROW_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFFCE5CD",
)

UNEXPECTED_COLUMN_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFD9EAF7",
)

ZEBRA_FILL = PatternFill(
    fill_type="solid",
    fgColor="FFF7F7F7",
)

HEADER_FILL = PatternFill(
    fill_type="solid",
    fgColor="FF44546A",
)

HEADER_FONT = Font(
    bold=True,
    color="FFFFFFFF",
)


def add_or_append_comment(cell, text: str) -> None:
    """
    Add a validation comment to a cell.

    If the cell already contains a Data Quality Toolkit comment,
    append the new issue instead of overwriting the existing one.
    """
    if cell.comment is None:
        comment_text = text
    else:
        comment_text = f"{cell.comment.text}\n{text}"

    cell.comment = Comment(
        comment_text,
        "Data Quality Toolkit",
    )


def style_source_worksheet(worksheet) -> None:
    """
    Apply general readability formatting to the source worksheet.
    """
    # Style header row.
    for cell in worksheet[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    # Apply subtle zebra striping to alternating data rows.
    for row_number in range(2, worksheet.max_row + 1):
        if row_number % 2 == 0:
            for column_number in range(
                1,
                worksheet.max_column + 1,
            ):
                worksheet.cell(
                    row=row_number,
                    column=column_number,
                ).fill = ZEBRA_FILL

    # Keep headers visible while scrolling.
    worksheet.freeze_panes = "A2"

    # Enable filtering across the source data.
    worksheet.auto_filter.ref = worksheet.dimensions

    # Automatically size columns.
    for column_number in range(
        1,
        worksheet.max_column + 1,
    ):
        max_length = 0

        for row_number in range(
            1,
            worksheet.max_row + 1,
        ):
            value = worksheet.cell(
                row=row_number,
                column=column_number,
            ).value

            if value is not None:
                max_length = max(
                    max_length,
                    len(str(value)),
                )

        column_letter = get_column_letter(column_number)

        worksheet.column_dimensions[
            column_letter
        ].width = min(
            max(max_length + 5, 12),
            50,
        )


def add_legend_sheet(workbook) -> None:
    """
    Add a legend explaining validation highlight colors.
    """
    if "Legend" in workbook.sheetnames:
        del workbook["Legend"]

    legend = workbook.create_sheet("Legend")

    legend.append(
        [
            "Highlight",
            "Meaning",
        ]
    )

    legend.append(
        [
            "",
            "Missing required value",
        ]
    )

    legend.append(
        [
            "",
            "Invalid value",
        ]
    )

    legend.append(
        [
            "",
            "Duplicate row",
        ]
    )

    legend.append(
        [
            "",
            "Unexpected column",
        ]
    )

    legend["A2"].fill = MISSING_VALUE_FILL
    legend["A3"].fill = INVALID_VALUE_FILL
    legend["A4"].fill = DUPLICATE_ROW_FILL
    legend["A5"].fill = UNEXPECTED_COLUMN_FILL

    for cell in legend[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    legend.column_dimensions["A"].width = 14
    legend.column_dimensions["B"].width = 30

    legend.freeze_panes = "A2"


def annotate_workbook(
    input_path: str | Path,
    result: ValidationResult,
    output_path: str | Path,
) -> None:
    """
    Create a reviewed copy of an Excel workbook with validation
    issues highlighted and explained.

    Args:
        input_path: Existing XLSX workbook.
        result: Validation issues detected for the workbook data.
        output_path: Destination for the annotated workbook.
    """
    source = Path(input_path)
    destination = Path(output_path)

    if not source.exists():
        raise FileNotFoundError(
            f"Input workbook not found: {source}"
        )

    if source.suffix.lower() != ".xlsx":
        raise ValueError(
            "Annotated workbook output currently requires "
            "an .xlsx input file."
        )

    if destination.suffix.lower() != ".xlsx":
        raise ValueError(
            "Annotated workbook output must use "
            "the .xlsx extension."
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    copy2(
        source,
        destination,
    )

    workbook = load_workbook(destination)
    worksheet = workbook.active

    header_columns = {
        cell.value: cell.column
        for cell in worksheet[1]
        if cell.value is not None
    }

    # Apply normal workbook styling first.
    # Validation colors are applied afterward so they take priority.
    style_source_worksheet(worksheet)

    # Duplicate rows are highlighted first.
    # Specific cell-level problems can then override the row color.
    for row_index in result.duplicate_rows:
        excel_row = source_row_number(row_index)

        for column_number in range(
            1,
            worksheet.max_column + 1,
        ):
            worksheet.cell(
                row=excel_row,
                column=column_number,
            ).fill = DUPLICATE_ROW_FILL

        first_cell = worksheet.cell(
            row=excel_row,
            column=1,
        )

        add_or_append_comment(
            first_cell,
            "Duplicate record detected.",
        )

    # Missing values override zebra or duplicate shading.
    for column, rows in result.missing_values.items():
        column_number = header_columns.get(column)

        if column_number is None:
            continue

        for row_index in rows:
            cell = worksheet.cell(
                row=source_row_number(row_index),
                column=column_number,
            )

            cell.fill = MISSING_VALUE_FILL

            add_or_append_comment(
                cell,
                "Missing required value.",
            )

    # Invalid values receive the highest cell-level priority.
    for column, rows in result.invalid_values.items():
        column_number = header_columns.get(column)

        if column_number is None:
            continue

        for row_index in rows:
            cell = worksheet.cell(
                row=source_row_number(row_index),
                column=column_number,
            )

            cell.fill = INVALID_VALUE_FILL

            add_or_append_comment(
                cell,
                f"Invalid value: {cell.value!s}",
            )

    # Unexpected columns override the normal header styling.
    for column in result.unexpected_columns:
        column_number = header_columns.get(column)

        if column_number is None:
            continue

        header_cell = worksheet.cell(
            row=1,
            column=column_number,
        )

        header_cell.fill = UNEXPECTED_COLUMN_FILL
        header_cell.font = Font(
            bold=True,
            color="FF000000",
        )

        add_or_append_comment(
            header_cell,
            "Unexpected column: not defined in the expected schema.",
        )

    add_legend_sheet(workbook)

    workbook.save(destination)