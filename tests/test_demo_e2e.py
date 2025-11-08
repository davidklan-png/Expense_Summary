"""End-to-End BDD tests for demo workflow.

This module tests the complete user journey from demo generation to file processing,
simulating real-world usage scenarios including global installations with pipx/pip.
"""

import csv
from pathlib import Path

import pytest
from typer.testing import CliRunner

from saisonxform.cli import app

runner = CliRunner()


class TestDemoEndToEndWorkflow:
    """
    BDD Scenario: User runs demo and processes sample files successfully

    GIVEN a user has installed saisonxform globally (via pipx/pip)
    WHEN they generate demo files and process them
    THEN they should see processed CSV and HTML outputs
    AND the files should be archived correctly
    """

    def test_complete_demo_workflow_with_explicit_config(self, tmp_path):
        """
        Complete demo workflow: generate → process → verify

        This test simulates the exact user workflow described in README:
        1. sf demo -o /some/directory
        2. sf --config /some/directory/config.toml --verbose
        3. Verify outputs and archival
        """
        # ========================================================================
        # GIVEN: User wants to try the demo in an isolated directory
        # ========================================================================
        demo_dir = tmp_path / "user-demo-test"

        # ========================================================================
        # WHEN: User generates demo files
        # ========================================================================
        result = runner.invoke(app, ["demo", "--output", str(demo_dir)])

        # THEN: Demo generation should succeed
        assert result.exit_code == 0
        assert "✅ Demo files created successfully!" in result.stdout
        assert demo_dir.exists()

        # AND: All required directories should be created
        assert (demo_dir / "Input").exists()
        assert (demo_dir / "Reference").exists()
        assert (demo_dir / "Output").exists()

        # AND: Sample files should be present
        sample_csv = demo_dir / "Input" / "202510_sample.csv"
        namelist = demo_dir / "Reference" / "NameList.csv"
        config_file = demo_dir / "config.toml"

        assert sample_csv.exists()
        assert namelist.exists()
        assert config_file.exists()

        # AND: Sample CSV should have expected structure
        with open(sample_csv, encoding="utf-8-sig") as f:
            lines = f.readlines()
            # Should have header + 5 transactions
            assert len(lines) == 6  # 1 header + 5 data rows
            assert "利用日,ご利用店名及び商品名,利用金額,備考" in lines[0]

        # AND: NameList should have attendees
        with open(namelist, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            attendees = list(reader)
            # Demo creates 8 attendees
            assert len(attendees) == 8
            assert all("ID" in a and "Name" in a for a in attendees)

        # AND: config.toml should have relative paths
        config_content = config_file.read_text()
        assert 'input_dir = "Input"' in config_content
        assert 'reference_dir = "Reference"' in config_content
        assert 'output_dir = "Output"' in config_content
        assert 'archive_dir = "Archive"' in config_content

        # ========================================================================
        # WHEN: User processes demo files with explicit config path
        # ========================================================================
        # This simulates: sf --config /path/to/demo/config.toml --verbose
        result = runner.invoke(
            app,
            [
                "--config", str(config_file),
                "--verbose",
            ]
        )

        # THEN: Processing should succeed
        assert result.exit_code == 0
        assert "Processing complete" in result.stdout
        assert "Processed: 1" in result.stdout
        assert "Errors: 0" in result.stdout

        # AND: Config paths should be resolved relative to config.toml location
        assert str(demo_dir / "Input") in result.stdout
        assert str(demo_dir / "Reference") in result.stdout
        assert str(demo_dir / "Output") in result.stdout

        # AND: Output files should be created
        output_csv = demo_dir / "Output" / "202510_sample.csv"
        output_html = demo_dir / "Output" / "202510_sample.html"

        assert output_csv.exists()
        assert output_html.exists()

        # AND: Output CSV should have attendee columns added
        with open(output_csv, encoding="utf-8-sig") as f:
            header = f.readline()
            assert "出席者" in header
            assert "ID1" in header
            assert "ID8" in header

            # Verify data rows have attendee assignments
            for line in f:
                if line.strip():
                    fields = line.split(",")
                    # Lines with 会議費/接待費 should have attendees
                    if "会議費" in line or "接待費" in line:
                        # Should have non-empty 出席者 column
                        assert len(fields) > 4  # Original + 出席者 + ID1-ID8

        # AND: HTML report should contain expected elements
        html_content = output_html.read_text(encoding="utf-8")
        assert "会議費" in html_content or "接待費" in html_content
        # HTML contains attendee information
        assert "ID:" in html_content
        assert "参加者一覧" in html_content or "attendee" in html_content.lower()

        # AND: Input file should be archived
        archived_file = demo_dir / "Archive" / "202510" / "202510_sample.csv"
        assert archived_file.exists()

        # AND: Original input file should be moved (not in Input anymore)
        assert not sample_csv.exists()

    def test_demo_workflow_with_cwd_in_demo_directory(self, tmp_path, monkeypatch):
        """
        Alternative workflow: cd into demo directory and run without --config

        This simulates:
        1. sf demo
        2. cd saisonxform-demo
        3. sf --verbose  (config.toml auto-detected)
        """
        # ========================================================================
        # GIVEN: User generates demo in current directory
        # ========================================================================
        monkeypatch.chdir(tmp_path)

        # Generate demo with default output
        result = runner.invoke(app, ["demo"], input="y\n")
        assert result.exit_code == 0

        demo_dir = tmp_path / "saisonxform-demo"
        assert demo_dir.exists()

        # ========================================================================
        # WHEN: User changes to demo directory
        # ========================================================================
        monkeypatch.chdir(demo_dir)

        # AND: Runs sf without explicit --config (should auto-detect)
        result = runner.invoke(app, ["--verbose"])

        # THEN: Processing should succeed with auto-detected config
        assert result.exit_code == 0
        assert "Processing complete" in result.stdout

        # AND: Paths should be resolved relative to current directory
        # (Since cwd is demo_dir and config.toml is there)
        assert "Input" in result.stdout
        assert "Reference" in result.stdout
        assert "Output" in result.stdout

    def test_demo_workflow_handles_missing_config_gracefully(self, tmp_path):
        """
        Edge case: Running without config.toml should use defaults

        GIVEN no config.toml exists
        WHEN user runs with explicit paths
        THEN processing should succeed using CLI arguments
        """
        # Create manual directory structure (no demo)
        input_dir = tmp_path / "Input"
        reference_dir = tmp_path / "Reference"
        output_dir = tmp_path / "Output"

        input_dir.mkdir()
        reference_dir.mkdir()
        output_dir.mkdir()

        # Create minimal CSV with a unique month to avoid conflicts with other tests
        # Using 202512 which shouldn't conflict
        sample_csv = input_dir / "202512_test.csv"
        sample_csv.write_text(
            "利用日,ご利用店名及び商品名,利用金額,備考\n"
            "2025-12-01,テスト,10000,会議費\n",
            encoding="utf-8-sig"
        )

        # Create minimal NameList with at least IDs 1 and 2 (for weighted selection)
        namelist = reference_dir / "NameList.csv"
        namelist.write_text(
            "ID,Name,Title,Company\n"
            "1,テスト太郎,部長,テスト株式会社\n"
            "2,テスト花子,課長,テスト株式会社\n"
            "3,テスト一郎,主任,テスト株式会社\n",
            encoding="utf-8"
        )

        # WHEN: Process with explicit paths (no config.toml)
        result = runner.invoke(
            app,
            [
                "--input", str(input_dir),
                "--reference", str(reference_dir),
                "--output", str(output_dir),
            ]
        )

        # THEN: Should succeed even without config.toml
        assert result.exit_code == 0, f"Failed with: {result.stdout}"
        assert "Processing complete" in result.stdout

    def test_demo_workflow_with_force_reprocessing(self, tmp_path):
        """
        Workflow: Process → Archive → Force reprocess

        GIVEN demo files have been processed and archived
        WHEN user tries to process the same month again
        THEN should error unless --force is used
        """
        # Setup and initial processing
        demo_dir = tmp_path / "force-test-demo"
        runner.invoke(app, ["demo", "--output", str(demo_dir)])

        config_file = demo_dir / "config.toml"

        # First processing
        result = runner.invoke(app, ["--config", str(config_file)])
        assert result.exit_code == 0

        # Restore the archived file to Input for reprocessing attempt
        archived = demo_dir / "Archive" / "202510" / "202510_sample.csv"
        input_file = demo_dir / "Input" / "202510_sample.csv"

        # Copy back (simulating user wants to reprocess)
        import shutil
        shutil.copy(archived, input_file)

        # WHEN: Try to process same month without --force
        result = runner.invoke(
            app,
            ["--config", str(config_file), "--month", "202510"]
        )

        # THEN: Should error (already archived)
        assert result.exit_code == 1
        assert "already been archived" in result.stdout.lower()

        # WHEN: Process with --force flag
        result = runner.invoke(
            app,
            ["--config", str(config_file), "--month", "202510", "--force"]
        )

        # THEN: Should succeed
        assert result.exit_code == 0
        assert "Processing complete" in result.stdout

    def test_demo_csv_content_quality(self, tmp_path):
        """
        Verify demo generates realistic and valid data

        GIVEN demo is generated
        THEN sample CSV should have:
        - Mix of 会議費 and 接待費 transactions
        - Some non-relevant transactions (for filtering test)
        - Realistic amounts and dates
        - Proper UTF-8 encoding
        """
        demo_dir = tmp_path / "quality-test"
        runner.invoke(app, ["demo", "--output", str(demo_dir)])

        sample_csv = demo_dir / "Input" / "202510_sample.csv"

        with open(sample_csv, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            transactions = list(reader)

        # Should have exactly 5 transactions
        assert len(transactions) == 5

        # Should have mix of expense types
        remarks = [t["備考"] for t in transactions]
        assert "会議費" in remarks
        assert "接待費" in remarks

        # Should have at least one non-relevant transaction
        assert any(remark not in ["会議費", "接待費"] for remark in remarks)

        # All should have required columns
        for transaction in transactions:
            assert "利用日" in transaction
            assert "ご利用店名及び商品名" in transaction
            assert "利用金額" in transaction
            assert "備考" in transaction

            # Amounts should be numeric
            amount = transaction["利用金額"]
            assert amount.isdigit() or amount.replace(",", "").isdigit()

    def test_demo_namelist_quality(self, tmp_path):
        """
        Verify demo NameList has sufficient variety

        GIVEN demo is generated
        THEN NameList should have:
        - 8 unique attendees (enough for max_attendees)
        - Proper ID, Name, Title, Company structure
        - At least ID 1 and ID 2 (for weighted selection)
        """
        demo_dir = tmp_path / "namelist-test"
        runner.invoke(app, ["demo", "--output", str(demo_dir)])

        namelist = demo_dir / "Reference" / "NameList.csv"

        with open(namelist, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            attendees = list(reader)

        # Should have 8 attendees (matches max_attendees default)
        assert len(attendees) == 8

        # Should have unique IDs
        ids = [a["ID"] for a in attendees]
        assert len(set(ids)) == len(ids)

        # Should include ID 1 and 2 (for weighted primary selection)
        assert "1" in ids
        assert "2" in ids

        # All should have complete data
        for attendee in attendees:
            assert attendee["ID"]
            assert attendee["Name"]
            assert attendee["Title"]
            assert attendee["Company"]

    def test_demo_config_has_all_required_sections(self, tmp_path):
        """
        Verify generated config.toml is complete and valid

        GIVEN demo is generated
        THEN config.toml should have:
        - [paths] section with all 4 directories
        - [processing] section with min/max attendees
        - [processing.primary_id_weights] with ID 1 and 2
        """
        demo_dir = tmp_path / "config-test"
        runner.invoke(app, ["demo", "--output", str(demo_dir)])

        config_file = demo_dir / "config.toml"
        config_content = config_file.read_text()

        # Should have [paths] section
        assert "[paths]" in config_content
        assert 'input_dir = "Input"' in config_content
        assert 'reference_dir = "Reference"' in config_content
        assert 'output_dir = "Output"' in config_content
        assert 'archive_dir = "Archive"' in config_content

        # Should have [processing] section
        assert "[processing]" in config_content
        assert "min_attendees" in config_content
        assert "max_attendees" in config_content

        # Should have primary ID weights
        assert "[processing.primary_id_weights]" in config_content
        assert '"2"' in config_content  # 90% weight
        assert '"1"' in config_content  # 10% weight

    def test_demo_directory_structure_matches_documentation(self, tmp_path):
        """
        Verify demo structure matches README documentation

        The README shows this structure:
        ./saisonxform-demo/
        ├── Input/202510_sample.csv
        ├── Reference/NameList.csv
        ├── Output/
        └── config.toml
        """
        demo_dir = tmp_path / "structure-test"
        result = runner.invoke(app, ["demo", "--output", str(demo_dir)])

        # Verify structure from README
        assert (demo_dir / "Input" / "202510_sample.csv").exists()
        assert (demo_dir / "Reference" / "NameList.csv").exists()
        assert (demo_dir / "Output").exists()
        assert (demo_dir / "config.toml").exists()

        # Output should be empty initially
        output_files = list((demo_dir / "Output").iterdir())
        assert len(output_files) == 0

        # Structure should be mentioned in output
        assert "Input/" in result.stdout
        assert "Reference/" in result.stdout
        assert "Output/" in result.stdout
        assert "config.toml" in result.stdout
