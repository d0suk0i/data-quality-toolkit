from openpyxl import Workbook, load_workbook

from src.data_quality_toolkit.annotator import annotate_workbook
from src.data_quality_toolkit.validator import ValidationResult


def test_annotate_workbook_highlights_validation_issues(tmp_path):
    source_path = tmp_path / "source.xlsx"
    output_path = tmp_path / "reviewed.xlsx"

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(
        [
            "id",
            "name",
            "email",
            "employment_type",
            "extra",
        ]
    )

    sheet.append(
        [
            101,
            "Alice",
            None,
            "full-time",
            "A",
        ]
    )

    sheet.append(
        [
            102,
            "Bob",
            "bob@example.com",
            "temporary",
            "B",
        ]
    )

    sheet.append(
        [
            102,
            "Bob",
            "bob@example.com",
            "contract",
            "C",
        ]
    )

    workbook.save(source_path)

    result = ValidationResult(
        unexpected_columns=["extra"],
        missing_values={
            "email": [0],
        },
        invalid_values={
            "employment_type": [1],
        },
        duplicate_rows=[2],
    )

    annotate_workbook(
        input_path=source_path,
        result=result,
        output_path=output_path,
    )

    reviewed = load_workbook(output_path)
    reviewed_sheet = reviewed.active

    assert output_path.exists()

    # Original data is preserved.
    assert reviewed_sheet["A2"].value == 101
    assert reviewed_sheet["B3"].value == "Bob"

    # Missing email.
    assert reviewed_sheet["C2"].fill.fill_type == "solid"

    # Invalid employment type.
    assert reviewed_sheet["D3"].fill.fill_type == "solid"

    # Duplicate row.
    assert reviewed_sheet["A4"].fill.fill_type == "solid"
    assert reviewed_sheet["E4"].fill.fill_type == "solid"

    # Unexpected column header.
    assert reviewed_sheet["E1"].fill.fill_type == "solid"

def test_annotated_workbook_includes_legend_sheet(tmp_path):
    source_path = tmp_path / "source.xlsx"
    output_path = tmp_path / "reviewed.xlsx"

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(
        [
            "id",
            "name",
            "email",
            "employment_type",
            "extra",
        ]
    )

    sheet.append(
        [
            101,
            "Alice",
            None,
            "temporary",
            "A",
        ]
    )

    workbook.save(source_path)

    result = ValidationResult(
        unexpected_columns=["extra"],
        missing_values={"email": [0]},
        invalid_values={"employment_type": [0]},
    )

    annotate_workbook(
        input_path=source_path,
        result=result,
        output_path=output_path,
    )

    reviewed = load_workbook(output_path)

    assert "Legend" in reviewed.sheetnames

    legend = reviewed["Legend"]

    assert legend["A1"].value == "Highlight"
    assert legend["B1"].value == "Meaning"

    assert legend["B2"].value == "Missing required value"
    assert legend["B3"].value == "Invalid value"
    assert legend["B4"].value == "Duplicate row"
    assert legend["B5"].value == "Unexpected column"

def test_specific_cell_issue_overrides_duplicate_row_fill(tmp_path):
    source_path = tmp_path / "source.xlsx"
    output_path = tmp_path / "reviewed.xlsx"

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(
        [
            "id",
            "employment_type",
        ]
    )

    sheet.append(
        [
            101,
            "full-time",
        ]
    )

    sheet.append(
        [
            101,
            "temporary",
        ]
    )

    workbook.save(source_path)

    result = ValidationResult(
        duplicate_rows=[1],
        invalid_values={
            "employment_type": [1],
        },
    )

    annotate_workbook(
        input_path=source_path,
        result=result,
        output_path=output_path,
    )

    reviewed = load_workbook(output_path)
    sheet = reviewed.active

    duplicate_fill = sheet["A3"].fill.fgColor.rgb
    invalid_fill = sheet["B3"].fill.fgColor.rgb

    assert duplicate_fill != invalid_fill
    assert sheet["A3"].fill.fill_type == "solid"
    assert sheet["B3"].fill.fill_type == "solid"

def test_annotated_workbook_polish(tmp_path):
    source_path = tmp_path / "source.xlsx"
    output_path = tmp_path / "reviewed.xlsx"

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(
        [
            "id",
            "name",
            "email",
            "employment_type",
            "extra",
        ]
    )

    sheet.append(
        [
            101,
            "Alice",
            "alice@example.com",
            "full-time",
            "A",
        ]
    )

    sheet.append(
        [
            102,
            "Bob",
            None,
            "part-time",
            "B",
        ]
    )

    sheet.append(
        [
            103,
            "Charlie",
            "charlie@example.com",
            "contract",
            "C",
        ]
    )

    sheet.append(
        [
            103,
            "Charlie",
            "charlie@example.com",
            "temporary",
            "D",
        ]
    )

    workbook.save(source_path)

    result = ValidationResult(
        unexpected_columns=["extra"],
        missing_values={
            "email": [1],
        },
        duplicate_rows=[3],
        invalid_values={
            "employment_type": [3],
        },
    )

    annotate_workbook(
        input_path=source_path,
        result=result,
        output_path=output_path,
    )

    reviewed = load_workbook(output_path)
    sheet = reviewed.active

    # Readability features.
    assert sheet.freeze_panes == "A2"
    assert sheet.auto_filter.ref is not None

    # Zebra shading exists on an ordinary row.
    assert sheet["A2"].fill.fill_type == "solid"

    # Missing value is highlighted and explained.
    assert sheet["C3"].fill.fill_type == "solid"
    assert sheet["C3"].comment is not None
    assert "Missing required value" in sheet["C3"].comment.text

    # Duplicate row is highlighted.
    assert sheet["A5"].fill.fill_type == "solid"
    assert sheet["A5"].comment is not None
    assert "Duplicate record" in sheet["A5"].comment.text

    # Invalid cell overrides duplicate-row shading.
    assert sheet["D5"].fill.fgColor.rgb != sheet["A5"].fill.fgColor.rgb
    assert sheet["D5"].comment is not None
    assert "temporary" in sheet["D5"].comment.text

    # Unexpected header is highlighted and explained.
    assert sheet["E1"].comment is not None
    assert "Unexpected column" in sheet["E1"].comment.text

    # Legend remains present.
    assert "Legend" in reviewed.sheetnames