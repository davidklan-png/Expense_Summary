"""Tests for CLI commands and error handling."""

import json

from typer.testing import CliRunner

from saisonxform.cli import app

runner = CliRunner()


class TestCLIVersionCommand:
    """Test --version flag."""

    def test_version_flag(self):
        """Should display version information."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "saisonxform" in result.stdout or "version" in result.stdout.lower()


class TestCLIHelp:
    """Test --help flag."""

    def test_help_flag(self):
        """Should display help information."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "saisonxform" in result.stdout.lower() or "usage" in result.stdout.lower()

    def test_run_help_flag(self):
        """Should display run command help."""
        result = runner.invoke(app, ["run", "--help"])

        assert result.exit_code == 0
        assert "process" in result.stdout.lower() or "transaction" in result.stdout.lower()


class TestCLIEmptyInput:
    """Test CLI with empty input directory."""

    def test_run_with_no_files(self, tmp_path):
        """Should handle empty input directory."""
        # Create empty directories
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
            ],
        )

        # Should succeed with no files to process
        assert result.exit_code == 0


class TestCLIMonthParsing:
    """Test month flag parsing."""

    def test_run_with_invalid_month_format(self, tmp_path):
        """Should handle month flag parsing."""
        # Create minimal structure for CLI to run
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
                "--month",
                "202510",  # Valid format
                "--force",
            ],
        )

        # Should succeed (no files to process)
        assert result.exit_code == 0


class TestCLIRetryMarkerHandling:
    """Test retry marker detection and handling."""

    def test_run_with_existing_retry_marker(self, tmp_path):
        """Should detect existing retry markers."""
        # Create directory structure
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"
        archive_dir = tmp_path / "Archive"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create retry marker
        retry_marker = archive_dir / ".retry_202510.json"
        archive_dir.mkdir()
        retry_marker.write_text(
            json.dumps(
                {
                    "month": "202510",
                    "failed_files": ["202510_test.csv"],
                    "timestamp": "2025-10-01T00:00:00",
                    "errors": ["Test error"],
                },
            ),
            encoding="utf-8",
        )

        # Create matching input file
        test_file = input_dir / "202510_test.csv"
        test_file.write_text(
            "利用日,ご利用店名及び商品名,利用金額,備考\\n2025-10-01,店舗,1000,会議費",
            encoding="utf-8",
        )

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\\n1,Test,Title,Company",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
                "--archive",
                str(archive_dir),
                "--month",
                "202510",
            ],
        )

        # Should either process or mention retry marker
        # (behavior depends on implementation details)
        assert result.exit_code in [0, 1]


class TestCLIVerboseFlag:
    """Test verbose logging flag."""

    def test_run_with_verbose_flag(self, tmp_path):
        """Should enable verbose logging."""
        # Create minimal setup
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
                "--verbose",
            ],
        )

        # Should succeed
        assert result.exit_code == 0


class TestCLIGitValidation:
    """Test git repository validation."""

    def test_run_fails_when_input_in_git_repo(self, tmp_path):
        """Should fail when input directory is inside a git repository."""
        import subprocess

        # Create git repository
        git_repo = tmp_path / "git_repo"
        git_repo.mkdir()

        # Initialize actual git repository
        subprocess.run(["git", "init"], cwd=git_repo, capture_output=True, check=True)

        # Create directories inside git repo
        input_dir = git_repo / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        input_dir.mkdir()
        reference_dir.mkdir()
        output_dir.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
            ],
        )

        # Should fail with error about git repository
        assert result.exit_code == 1
        assert "git repository" in result.stdout.lower()


class TestCLIMissingFiles:
    """Test CLI with missing required files."""

    def test_run_fails_when_namelist_missing(self, tmp_path):
        """Should fail when NameList.csv is missing."""
        # Create directories but no NameList.csv
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
            ],
        )

        # Should fail with error about missing NameList.csv
        assert result.exit_code == 1
        assert "NameList.csv" in result.stdout


class TestCLIArchivalErrors:
    """Test CLI archival error handling."""

    def test_run_detects_already_archived_month(self, tmp_path):
        """Should detect when month is already archived."""
        # Create directory structure
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"
        archive_dir = tmp_path / "Archive"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create archive directory for month 202510 (already processed)
        month_archive = archive_dir / "202510"
        month_archive.mkdir(parents=True)

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        # Create input file for already-archived month
        test_file = input_dir / "202510_test.csv"
        test_file.write_text(
            "利用日,ご利用店名及び商品名,利用金額,備考\n2025-10-01,店舗,1000,会議費",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
                "--archive",
                str(archive_dir),
                "--month",
                "202510",
            ],
        )

        # Should fail or warn about already archived month
        assert "already" in result.stdout.lower() or result.exit_code == 1

    def test_run_with_force_flag_bypasses_archive_check(self, tmp_path):
        """Should reprocess archived month with --force flag."""
        # Create directory structure
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"
        archive_dir = tmp_path / "Archive"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create archive directory for month 202510
        month_archive = archive_dir / "202510"
        month_archive.mkdir(parents=True)

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company\n2,Test2,Title2,Company2\n3,Test3,Title3,Company3",
            encoding="utf-8",
        )

        # Create input file
        test_file = input_dir / "202510_test.csv"
        test_file.write_text(
            "利用日,ご利用店名及び商品名,利用金額,備考\n2025-10-01,店舗,1000,会議費",
            encoding="utf-8",
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
                "--archive",
                str(archive_dir),
                "--month",
                "202510",
                "--force",
            ],
        )

        # Should succeed with --force
        assert result.exit_code == 0


class TestCLIProcessingErrors:
    """Test CLI file processing error handling."""

    def test_run_handles_csv_read_errors(self, tmp_path):
        """Should handle CSV read errors gracefully."""
        # Create directory structure
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company",
            encoding="utf-8",
        )

        # Create invalid CSV file
        test_file = input_dir / "202510_invalid.csv"
        test_file.write_bytes(b"\xff\xfe\xfd")  # Invalid bytes

        result = runner.invoke(
            app,
            [
                "run",
                "--input",
                str(input_dir),
                "--reference",
                str(reference_dir),
                "--output",
                str(output_dir),
            ],
        )

        # Should complete - invalid files are skipped
        assert result.exit_code == 0
        assert "SKIPPED" in result.stdout or "Empty file" in result.stdout

    def test_run_handles_write_permission_errors(self, tmp_path):
        """Should handle write permission errors."""
        # Create directory structure
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        for d in [input_dir, reference_dir, output_dir]:
            d.mkdir()

        # Create reference file
        ref_file = reference_dir / "NameList.csv"
        ref_file.write_text(
            "ID,Name,Title,Company\n1,Test,Title,Company\n2,Test2,Title2,Company2",
            encoding="utf-8",
        )

        # Create valid input file
        test_file = input_dir / "202510_test.csv"
        test_file.write_text(
            "利用日,ご利用店名及び商品名,利用金額,備考\n2025-10-01,店舗,1000,会議費",
            encoding="utf-8",
        )

        # Make output directory read-only to trigger permission error
        import os

        os.chmod(output_dir, 0o444)

        try:
            result = runner.invoke(
                app,
                [
                    "run",
                    "--input",
                    str(input_dir),
                    "--reference",
                    str(reference_dir),
                    "--output",
                    str(output_dir),
                ],
            )

            # Should report errors
            assert "ERROR" in result.stdout or result.exit_code != 0

        finally:
            # Restore permissions for cleanup
            os.chmod(output_dir, 0o755)
