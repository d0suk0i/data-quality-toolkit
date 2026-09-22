# Data Quality Toolkit

A Python command-line tool for validating CSV and Excel datasets against configurable data-quality rules.

The toolkit can detect common data problems such as missing columns, missing values, duplicate records, unexpected columns, and invalid categorical values.

Validation rules can be supplied through command-line arguments or reusable YAML configuration files.

## Features

- Load CSV and Excel (`.xlsx`) files
- Detect missing required columns
- Detect unexpected columns
- Detect missing values
- Detect duplicate rows
- Detect duplicates using selected key columns
- Validate values against allowed-value lists
- Configure validation rules using YAML
- Generate readable validation reports
- Return meaningful CLI exit codes
- Automated test suite with `pytest`

## Requirements

- Python 3.10+
- pandas
- openpyxl
- PyYAML

## Installation

Clone the repository:

```bash
git clone <repository-url>
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

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## Basic Usage

Validate required columns:

```bash
python -m src.data_quality_toolkit.cli data.csv --required id name email
```

Check duplicates using an ID column:

```bash
python -m src.data_quality_toolkit.cli data.csv --required id name --duplicate-key id
```

## YAML Configuration

Validation rules can also be stored in a YAML file.

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

Run validation using the configuration:

```bash
python -m src.data_quality_toolkit.cli samples/sample_jobs.csv --config config/job_rules.yaml
```

## Example Output

```text
Validation failed:
Missing values in 'email': rows 2
Duplicate rows: 3
Invalid values in 'employment_type': rows 3
```

A valid dataset produces:

```text
Validation passed: no issues found.
```

## Project Structure

```text
data-quality-toolkit/
├── config/
│   └── job_rules.yaml
├── samples/
│   └── sample_jobs.csv
├── src/
│   └── data_quality_toolkit/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── loader.py
│       ├── report.py
│       └── validator.py
├── tests/
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_loader.py
│   ├── test_report.py
│   └── test_validator.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Testing

Run the complete test suite:

```bash
python -m pytest -v
```

## Current Status

The current version provides the core validation engine and command-line interface.

Planned improvements include:

- Exportable validation reports
- Excel-formatted QA reports
- Additional validation rules
- Better configuration validation
- Batch file processing
- Summary statistics
- Improved CLI error handling

## License

This project is intended as a portfolio and learning project.