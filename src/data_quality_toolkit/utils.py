def source_row_number(row_index: int) -> int:
    """
    Convert a zero-based pandas row index to the corresponding
    source-file row number.

    Row 1 is assumed to contain column headers.
    """
    return int(row_index) + 2