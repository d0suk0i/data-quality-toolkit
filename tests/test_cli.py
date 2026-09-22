import pandas as pd

from src.data_quality_toolkit.cli import main


def test_cli_returns_success_for_valid_file(tmp_path, capsys):
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
            "email": [
                "alice@example.com",
                "bob@example.com",
            ],
        }
    )

    file_path = tmp_path / "valid.csv"
    data.to_csv(file_path, index=False)

    exit_code = main(
        [
            str(file_path),
            "--required",
            "name",
            "email",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Validation passed" in output


def test_cli_returns_failure_for_invalid_file(tmp_path, capsys):
    data = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
        }
    )

    file_path = tmp_path / "invalid.csv"
    data.to_csv(file_path, index=False)

    exit_code = main(
        [
            str(file_path),
            "--required",
            "name",
            "email",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Missing columns: email" in output