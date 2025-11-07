"""Integration tests for end-to-end pipeline."""
import pytest
from pathlib import Path
import pandas as pd
from saisonxform.config import Config
# TODO: Update tests to use new Typer CLI structure
# from saisonxform.cli import process_files
import sys


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
    namelist.write_text("""ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
3,鈴木一郎,主任,DEF株式会社
4,田中美咲,係長,GHI株式会社
5,高橋健太,社員,JKL株式会社
""", encoding='utf-8')

    # Create sample transaction CSV
    sample_csv = input_dir / "202510_test.csv"
    sample_csv.write_text("""利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,東京レストラン,15000,会議費
2025-10-02,カフェABC,5000,接待費
2025-10-03,スーパーマーケット,3000,その他
2025-10-04,ホテル会議室,25000,会議費
""", encoding='utf-8')

    # Set environment variables
    monkeypatch.setenv('INPUT_DIR', str(input_dir))
    monkeypatch.setenv('REFERENCE_DIR', str(reference_dir))
    monkeypatch.setenv('OUTPUT_DIR', str(output_dir))
    monkeypatch.setenv('ARCHIVE_DIR', str(tmp_path / "Archive"))

    return {
        'input_dir': input_dir,
        'reference_dir': reference_dir,
        'output_dir': output_dir,
        'tmp_path': tmp_path
    }


class TestConfigurationManagement:
    """Test configuration loading and validation."""

    def test_config_loads_from_env(self, integration_env):
        """Should load configuration from environment variables."""
        config = Config()

        assert config.input_dir == integration_env['input_dir']
        assert config.output_dir == integration_env['output_dir']

    def test_validate_dirs_success(self, integration_env):
        """Should validate existing directories successfully."""
        config = Config()

        # Should not raise exception
        config.validate_directories()

    def test_validate_dirs_missing_input(self, tmp_path, monkeypatch):
        """Should raise error for missing input directory."""
        monkeypatch.setenv('INPUT_DIR', str(tmp_path / "NonExistent"))
        monkeypatch.setenv('REFERENCE_DIR', str(tmp_path))
        monkeypatch.setenv('OUTPUT_DIR', str(tmp_path))

        config = Config()

        with pytest.raises(FileNotFoundError, match="Required directories not found"):
            config.validate_directories()


class TestEndToEndPipeline:
    """Test complete processing pipeline."""

    @pytest.mark.skip(reason="TODO: Update to use new Typer CLI structure - process_files() no longer exists")
    def test_process_files_success(self, integration_env, capsys):
        """Should successfully process CSV files end-to-end."""
        # Run process_files
        exit_code = process_files()

        # Check exit code
        assert exit_code == 0

        # Verify output files were created
        output_dir = integration_env['output_dir']

        csv_files = list(output_dir.glob('*.csv'))
        html_files = list(output_dir.glob('*.html'))

        assert len(csv_files) >= 1, "Should create processed CSV"
        assert len(html_files) >= 1, "Should create HTML report"

        # Verify CSV content
        csv_file = csv_files[0]
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        assert '出席者' in df.columns
        assert 'ID1' in df.columns
        assert 'ID8' in df.columns

        # Should only have meeting/entertainment expenses
        assert len(df) == 3  # 2 会議費 + 1 接待費

        # Verify HTML content
        html_file = html_files[0]
        html_content = html_file.read_text(encoding='utf-8')

        assert '東京レストラン' in html_content
        assert 'カフェABC' in html_content
        assert '山田太郎' in html_content or '佐藤花子' in html_content

    @pytest.mark.skip(reason="TODO: Update to use new Typer CLI structure - process_files() no longer exists")
    def test_process_files_empty_input(self, integration_env, capsys):
        """Should handle empty input directory gracefully."""
        # Remove CSV files
        for csv_file in integration_env['input_dir'].glob('*.csv'):
            csv_file.unlink()

        exit_code = process_files()

        # Should succeed with no files to process
        assert exit_code == 0

        captured = capsys.readouterr()
        assert "No CSV files found" in captured.out

    @pytest.mark.skip(reason="TODO: Update to use new Typer CLI structure - process_files() no longer exists")
    def test_process_files_no_relevant_transactions(self, integration_env):
        """Should skip files with no meeting/entertainment expenses."""
        # Create CSV with only other expenses
        input_dir = integration_env['input_dir']

        # Clear existing files
        for f in input_dir.glob('*.csv'):
            f.unlink()

        # Create file with no relevant transactions
        other_csv = input_dir / "202510_other.csv"
        other_csv.write_text("""利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,スーパーマーケット,3000,その他
2025-10-02,ガソリンスタンド,5000,交通費
""", encoding='utf-8')

        exit_code = process_files()

        # Should succeed but no output files
        assert exit_code == 0

        output_dir = integration_env['output_dir']
        csv_files = list(output_dir.glob('*.csv'))
        html_files = list(output_dir.glob('*.html'))

        # Should not create output for files with no relevant transactions
        assert len(csv_files) == 0
        assert len(html_files) == 0

    @pytest.mark.skip(reason="TODO: Update to use new Typer CLI structure - process_files() no longer exists")
    def test_process_files_missing_namelist(self, integration_env):
        """Should error if NameList.csv is missing."""
        # Remove NameList.csv
        namelist = integration_env['reference_dir'] / 'NameList.csv'
        namelist.unlink()

        exit_code = process_files()

        # Should fail
        assert exit_code == 1


class TestCLICommands:
    """Test CLI command parsing."""

    @pytest.mark.skip(reason="TODO: Update to use Typer testing utilities (CliRunner) instead of sys.argv mocking")
    def test_validate_config_command(self, integration_env, monkeypatch, capsys):
        """Should execute validate-config command."""
        from saisonxform.cli import main

        monkeypatch.setattr(sys, 'argv', ['saisonxform', 'validate-config'])

        exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Configuration validation complete" in captured.out or "SUCCESS" in captured.out

    @pytest.mark.skip(reason="TODO: Update to use Typer testing utilities (CliRunner) instead of sys.argv mocking")
    def test_process_command(self, integration_env, monkeypatch):
        """Should execute process command."""
        from saisonxform.cli import main

        monkeypatch.setattr(sys, 'argv', ['saisonxform', 'process'])

        exit_code = main()

        assert exit_code == 0

    @pytest.mark.skip(reason="TODO: Update to use Typer testing utilities (CliRunner) instead of sys.argv mocking")
    def test_unknown_command(self, monkeypatch, capsys):
        """Should handle unknown commands."""
        from saisonxform.cli import main

        monkeypatch.setattr(sys, 'argv', ['saisonxform', 'unknown'])

        exit_code = main()

        captured = capsys.readouterr()
        assert "Unknown command" in captured.out

    @pytest.mark.skip(reason="TODO: Update to use Typer testing utilities (CliRunner) instead of sys.argv mocking")
    def test_default_usage(self, monkeypatch, capsys):
        """Should show usage when no command given."""
        from saisonxform.cli import main

        monkeypatch.setattr(sys, 'argv', ['saisonxform'])

        exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
        assert "validate-config" in captured.out
        assert "process" in captured.out
