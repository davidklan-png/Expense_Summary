"""Integration tests for end-to-end pipeline."""

import pandas as pd
import pytest
from typer.testing import CliRunner

from saisonxform.cli import app
from saisonxform.config import Config

runner = CliRunner()


@pytest.fixture
def integration_env(tmp_path, monkeypatch):
    """Set up complete test environment with all directories."""
    # Create directory structure
    input_dir = tmp_path / "Input"
    reference_dir = tmp_path / "Reference"
    output_dir = tmp_path / "Output"

    input_dir.mkdir()
    reference_dir.mkdir()
    output_dir.mkdir()

    # Create sample NameList.csv
    namelist = reference_dir / "NameList.csv"
    namelist.write_text(
        """ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
3,鈴木一郎,主任,DEF株式会社
4,田中美咲,係長,GHI株式会社
5,高橋健太,社員,JKL株式会社
""",
        encoding="utf-8",
    )

    # Create sample transaction CSV
    sample_csv = input_dir / "202510_test.csv"
    sample_csv.write_text(
        """利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,東京レストラン,15000,会議費
2025-10-02,カフェABC,5000,接待費
2025-10-03,スーパーマーケット,3000,その他
2025-10-04,ホテル会議室,25000,会議費
""",
        encoding="utf-8",
    )

    # Set environment variables
    monkeypatch.setenv("INPUT_DIR", str(input_dir))
    monkeypatch.setenv("REFERENCE_DIR", str(reference_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("ARCHIVE_DIR", str(tmp_path / "Archive"))

    return {"input_dir": input_dir, "reference_dir": reference_dir, "output_dir": output_dir, "tmp_path": tmp_path}


class TestConfigurationManagement:
    """Test configuration loading and validation."""

    def test_config_loads_from_env(self, integration_env):
        """Should load configuration from environment variables."""
        config = Config()

        assert config.input_dir == integration_env["input_dir"]
        assert config.output_dir == integration_env["output_dir"]

    def test_validate_dirs_success(self, integration_env):
        """Should validate existing directories successfully."""
        config = Config()

        # Should not raise exception
        config.validate_directories()

    def test_validate_dirs_missing_input(self, tmp_path, monkeypatch):
        """Should raise error for missing input directory."""
        monkeypatch.setenv("INPUT_DIR", str(tmp_path / "NonExistent"))
        monkeypatch.setenv("REFERENCE_DIR", str(tmp_path))
        monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

        config = Config()

        with pytest.raises(FileNotFoundError, match="Required directories not found"):
            config.validate_directories()


class TestEndToEndPipeline:
    """Test complete processing pipeline."""

    def test_process_files_success(self, integration_env):
        """Should successfully process CSV files end-to-end."""
        # Run CLI command
        result = runner.invoke(app, ["run", "--force"])

        # Check exit code
        assert result.exit_code == 0

        # Verify output files were created
        output_dir = integration_env["output_dir"]

        csv_files = list(output_dir.glob("*.csv"))
        html_files = list(output_dir.glob("*.html"))

        assert len(csv_files) >= 1, "Should create processed CSV"
        assert len(html_files) >= 1, "Should create HTML report"

        # Verify CSV content (Phase 4: ALL rows preserved)
        csv_file = csv_files[0]
        df = pd.read_csv(csv_file, encoding="utf-8-sig")

        assert "出席者" in df.columns
        assert "ID1" in df.columns
        assert "ID8" in df.columns

        # Should have ALL rows (3 relevant + 1 non-relevant = 4 total)
        assert len(df) == 4

        # Check relevant rows have attendee data
        relevant_rows = df[df["備考"].str.contains("会議費|接待費", na=False)]
        assert len(relevant_rows) == 3
        assert all(relevant_rows["出席者"].notna())  # Has attendee count

        # Check non-relevant row has blank attendee data
        non_relevant = df[~df["備考"].str.contains("会議費|接待費", na=False)]
        assert len(non_relevant) == 1
        # Empty strings are read as NaN by pandas
        assert all(non_relevant["出席者"].isna() | (non_relevant["出席者"] == ""))

        # Verify HTML content
        html_file = html_files[0]
        html_content = html_file.read_text(encoding="utf-8")

        assert "東京レストラン" in html_content
        assert "カフェABC" in html_content
        assert "山田太郎" in html_content or "佐藤花子" in html_content

    def test_process_files_empty_input(self, integration_env):
        """Should handle empty input directory gracefully."""
        # Remove CSV files
        for csv_file in integration_env["input_dir"].glob("*.csv"):
            csv_file.unlink()

        result = runner.invoke(app, ["run"])

        # Should succeed with no files to process
        assert result.exit_code == 0
        assert "No CSV files found" in result.stdout

    def test_process_files_no_relevant_transactions(self, integration_env):
        """Should process files with no meeting/entertainment expenses (Phase 4: keep all rows)."""
        # Create CSV with only other expenses
        input_dir = integration_env["input_dir"]

        # Clear existing files
        for f in input_dir.glob("*.csv"):
            f.unlink()

        # Create file with no relevant transactions
        other_csv = input_dir / "202510_other.csv"
        other_csv.write_text(
            """利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,スーパーマーケット,3000,その他
2025-10-02,ガソリンスタンド,5000,交通費
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["run", "--force"])

        # Should succeed
        assert result.exit_code == 0

        output_dir = integration_env["output_dir"]
        csv_files = list(output_dir.glob("*.csv"))
        html_files = list(output_dir.glob("*.html"))

        # Phase 4: Should create CSV with all rows (attendee columns blank)
        assert len(csv_files) == 1
        df = pd.read_csv(csv_files[0], encoding="utf-8-sig")
        assert len(df) == 2  # Both rows preserved
        # Empty strings are read as NaN by pandas
        assert all(df["出席者"].isna() | (df["出席者"] == ""))  # All blank

        # No HTML report (no relevant transactions)
        assert len(html_files) == 0

    def test_process_files_missing_namelist(self, integration_env):
        """Should error if NameList.csv is missing."""
        # Remove NameList.csv
        namelist = integration_env["reference_dir"] / "NameList.csv"
        namelist.unlink()

        result = runner.invoke(app, ["run"])

        # Should fail
        assert result.exit_code == 1
        assert "NameList.csv not found" in result.stdout


class TestCLICommands:
    """Test CLI command parsing."""

    def test_validate_config_command(self, integration_env):
        """Should execute validate-config command."""
        result = runner.invoke(app, ["validate-config"])

        assert result.exit_code == 0
        assert "Configuration validation complete" in result.stdout or "SUCCESS" in result.stdout

    def test_run_with_month_flag(self, integration_env):
        """Should process specific month with --month flag."""
        result = runner.invoke(app, ["run", "--month", "202510", "--force"])

        assert result.exit_code == 0
        assert "202510" in result.stdout or "Found" in result.stdout

    def test_run_with_verbose_flag(self, integration_env):
        """Should show verbose output with --verbose flag."""
        result = runner.invoke(app, ["run", "--verbose", "--force"])

        assert result.exit_code == 0
        assert "Configuration Precedence" in result.stdout or "Detected encoding" in result.stdout

    def test_version_flag(self):
        """Should show version with --version flag."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "saisonxform version" in result.stdout

    def test_help_command(self):
        """Should show help message."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "Usage:" in result.stdout or "Commands:" in result.stdout
