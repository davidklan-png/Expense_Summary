"""Tests for edge cases and error conditions."""
from pathlib import Path

import pandas as pd
import pytest

from saisonxform.io import detect_encoding, find_header_row, read_csv_with_detection
from saisonxform.reporting import get_unique_attendees
from saisonxform.selectors import estimate_attendee_count, filter_relevant_transactions


class TestIOEdgeCases:
    """Test I/O edge cases."""

    def test_detect_encoding_file_not_exists(self, tmp_path):
        """Should handle non-existent files gracefully."""
        fake_file = tmp_path / "nonexistent.csv"

        # detect_encoding doesn't raise FileNotFoundError, it returns fallback
        # So we test that it returns a valid encoding even for non-existent files
        try:
            encoding = detect_encoding(fake_file)
            # Should return fallback encoding
            assert encoding in ["utf-8-sig", "utf-8", "cp932"]
        except FileNotFoundError:
            # Also acceptable behavior
            pass

    def test_find_header_beyond_row_10(self, tmp_path):
        """Should return None if header is beyond row 10."""
        test_file = tmp_path / "late_header.csv"
        lines = ["data"] * 11 + ["利用日,ご利用店名及び商品名,利用金額,備考"]
        test_file.write_text("\n".join(lines), encoding="utf-8")

        header_idx = find_header_row(test_file)

        # Should not find header beyond row 10
        assert header_idx is None

    def test_read_csv_nonexistent_file(self, tmp_path):
        """Should raise FileNotFoundError for missing file."""
        fake_file = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError):
            read_csv_with_detection(fake_file)

    def test_read_csv_encoding_fallback_chain(self, tmp_path):
        """Should try fallback encodings on UnicodeDecodeError."""
        test_file = tmp_path / "mixed.csv"

        # Write valid UTF-8 content
        test_file.write_text("利用日,ご利用店名及び商品名,利用金額,備考\ntest,data,1000,会議費", encoding="utf-8")

        # Read with explicit wrong encoding, should fallback
        df, encoding = read_csv_with_detection(test_file, encoding="ascii")

        # Should successfully read using fallback
        assert df is not None
        assert len(df) == 1


class TestSelectorEdgeCases:
    """Test selector edge cases."""

    def test_filter_transactions_missing_column(self):
        """Should return empty DataFrame if '備考' column missing."""
        df = pd.DataFrame({"利用日": ["2025-10-01"], "金額": [1000]})

        result = filter_relevant_transactions(df)

        assert len(result) == 0

    def test_estimate_attendees_large_amount(self):
        """Should respect max attendees even for large amounts."""
        for _ in range(20):
            count = estimate_attendee_count(amount=1000000, max_attendees=5)
            assert count <= 5

    def test_estimate_attendees_small_amount(self):
        """Should respect min attendees even for small amounts."""
        for _ in range(20):
            count = estimate_attendee_count(amount=1, min_attendees=3)
            assert count >= 3


class TestReportingEdgeCases:
    """Test reporting edge cases."""

    def test_get_unique_attendees_no_id_columns(self):
        """Should handle DataFrame without ID columns."""
        df = pd.DataFrame({"利用日": ["2025-10-01"], "金額": [1000]})

        attendee_ref = pd.DataFrame(
            {
                "ID": ["1", "2"],
                "Name": ["Test 1", "Test 2"],
                "Title": ["Title 1", "Title 2"],
                "Company": ["Company 1", "Company 2"],
            }
        )

        result = get_unique_attendees(df, attendee_ref)

        assert len(result) == 0
        assert list(result.columns) == ["ID", "Name", "Title", "Company"]

    def test_get_unique_attendees_all_empty_ids(self):
        """Should handle all empty ID values."""
        df = pd.DataFrame(
            {
                "ID1": ["", "", ""],
                "ID2": ["", "", ""],
                "ID3": ["", "", ""],
                "ID4": ["", "", ""],
                "ID5": ["", "", ""],
                "ID6": ["", "", ""],
                "ID7": ["", "", ""],
                "ID8": ["", "", ""],
            }
        )

        attendee_ref = pd.DataFrame(
            {
                "ID": ["1", "2"],
                "Name": ["Test 1", "Test 2"],
                "Title": ["Title 1", "Title 2"],
                "Company": ["Company 1", "Company 2"],
            }
        )

        result = get_unique_attendees(df, attendee_ref)

        assert len(result) == 0


class TestConfigEdgeCases:
    """Test configuration edge cases."""

    def test_config_with_relative_paths(self, tmp_path, monkeypatch):
        """Should resolve relative paths correctly."""
        from saisonxform.config import Config

        # Create test structure
        input_dir = tmp_path / "Input"
        output_dir = tmp_path / "Output"
        input_dir.mkdir()
        output_dir.mkdir()

        # Set relative paths
        monkeypatch.setenv("INPUT_DIR", "./Input")
        monkeypatch.setenv("REFERENCE_DIR", "./Reference")
        monkeypatch.setenv("OUTPUT_DIR", "./Output")

        # Change to tmp_path
        import os

        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            config = Config()

            # Paths should be resolved
            assert config.input_dir.is_absolute()
            assert config.output_dir.is_absolute()

        finally:
            os.chdir(old_cwd)

    def test_config_fallback_to_defaults(self, tmp_path, monkeypatch):
        """Should use defaults when no env vars set."""
        from saisonxform.config import Config

        # Clear environment variables
        for var in ["INPUT_DIR", "REFERENCE_DIR", "OUTPUT_DIR", "ARCHIVE_DIR"]:
            monkeypatch.delenv(var, raising=False)

        config = Config(project_root=tmp_path)

        # Should have default relative paths
        assert config.input_dir.name == "Input"
        assert config.output_dir.name == "Output"
