# Data Quality Toolkit

A lightweight Python tool for validating CSV and Excel datasets using reusable YAML rules.

Data Quality Toolkit is designed for practical spreadsheet and operational data QA. It can identify common data-quality issues, generate structured reports, and create annotated Excel workbooks that visually highlight problems.

## Features

- CSV and Excel (`.xlsx`) input
- Required-column validation
- Unexpected-column detection
- Missing-value detection
- Duplicate-row detection
- Duplicate detection using selected key columns
- Allowed-value validation
- YAML-based validation rules
- Human-readable terminal reports
- CSV issue reports
- Formatted Excel QA reports
- Annotated Excel workbook copies
- Source-file row numbers in reports
- Highlighted problem cells and rows
- Comments explaining validation issues
- Zebra-striped reviewed spreadsheets
- Frozen headers and filters
- Automatic column sizing
- Validation legend sheet
- Meaningful CLI exit codes
- Automated pytest test suite

## Installation

Clone the repository:

```bash
git clone https://github.com/d0suk0i/data-quality-toolkit.git
cd data-quality-toolkit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the application:

```bash
pip install -e .
```

For development and testing:

```bash
pip install -e ".[dev]"
```

## Command-Line Interface

After installation:

```bash
data-quality --help
```

Check the installed version:

```bash
data-quality --version
```

## Basic Validation

Validate required columns:

```bash
data-quality data.csv --required id name email
```

Check duplicates using an ID:

```bash
data-quality data.csv --required id name --duplicate-key id
```

## YAML Configuration

Reusable validation rules can be stored in YAML.

Example:

```yaml
required_columns:
  - id
  - name
  - email
  - employment_type

expected_columns:
  - id
  - name
  - email
  - employment_type

duplicate_subset:
  - id

allowed_values:
  employment_type:
    - full-time
    - part-time
    - contract
```

Run:

```bash
data-quality samples/sample_jobs.xlsx --config config/job_rules.yaml
```

## Report Export

Export issues to CSV:

```bash
data-quality samples/sample_jobs.xlsx \
  --config config/job_rules.yaml \
  --output validation_report.csv
```

Export a formatted Excel QA report:

```bash
data-quality samples/sample_jobs.xlsx \
  --config config/job_rules.yaml \
  --output validation_report.xlsx
```

The Excel report contains:

- `Summary` — validation status and issue counts
- `Issues` — individual problems with source-file row numbers

## Annotated Excel Workbooks

For Excel input files, Data Quality Toolkit can create a reviewed copy of the original workbook:

```bash
data-quality samples/sample_jobs.xlsx \
  --config config/job_rules.yaml \
  --annotated-output reviewed_sample_jobs.xlsx
```

The reviewed workbook includes:

- highlighted missing values
- highlighted invalid values
- highlighted duplicate rows
- highlighted unexpected columns
- comments explaining individual issues
- alternating row shading
- frozen headers
- autofilters
- automatic column sizing
- a legend explaining validation colors

Specific cell-level issues take priority over row-level highlighting, so multiple problems can remain visible on the same record.

## Combined Example

```bash
data-quality samples/sample_jobs.xlsx \
  --config config/job_rules.yaml \
  --output validation_report.xlsx \
  --annotated-output reviewed_sample_jobs.xlsx
```

This validates the source data, prints the result to the terminal, creates a structured QA report, and produces an annotated review workbook.

## Exit Codes

- `0` — validation completed with no issues
- `1` — validation completed and data-quality issues were found
- `2` — validation could not complete because of invalid input, configuration, or file errors

This makes the tool suitable for use in scripts and automated workflows.

## Project Structure

```text
data-quality-toolkit/
├── config/
│   └── job_rules.yaml
├── samples/
│   ├── sample_jobs.csv
│   └── sample_jobs.xlsx
├── src/
│   └── data_quality_toolkit/
│       ├── __init__.py
│       ├── __main__.py
│       ├── annotator.py
│       ├── cli.py
│       ├── config.py
│       ├── exporter.py
│       ├── loader.py
│       ├── report.py
│       ├── utils.py
│       └── validator.py
├── tests/
├── LICENSE
├── pyproject.toml
└── README.md
```

## Testing

Run the full test suite:

```bash
python -m pytest -v
```

## Current Version

**1.0.0**

The initial release focuses on practical CSV and Excel data-quality validation for local business and operational workflows.

Potential future improvements include batch processing, additional validation rules, multi-sheet validation, and graphical interfaces.

## License

MIT License