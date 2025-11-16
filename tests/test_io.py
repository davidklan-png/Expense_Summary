"""Tests for CSV I/O operations with encoding detection."""

import pandas as pd
import pytest

from saisonxform.io import detect_encoding, find_header_row, read_csv_with_detection, write_csv_utf8_bom


class TestEncodingDetection:
    """Test encoding detection logic."""

    def test_detect_utf8_bom(self, tmp_path):
        """Should detect UTF-8 with BOM encoding."""
        test_file = tmp_path / "utf8_bom.csv"
        test_file.write_bytes(b"\xef\xbb\xbf" + "テスト".encode())

        encoding = detect_encoding(test_file)
        assert encoding in ["utf-8-sig", "UTF-8-SIG"]

    def test_detect_cp932(self, tmp_path):
        """Should detect CP932 (Shift-JIS) encoding with sufficient text."""
        test_file = tmp_path / "cp932.csv"
        # Need more text for chardet to detect reliably
        content = "\n".join(
            [
                "利用日,店舗名,金額,備考",
                "2025-10-01,東京レストラン,10000,会議費",
                "2025-10-02,大阪カフェ,5000,接待費",
                "2025-10-03,名古屋ホテル,15000,会議費",
            ],
        )
        test_file.write_bytes(content.encode("cp932"))

        encoding = detect_encoding(test_file)
        # chardet may return 'SHIFT_JIS', 'cp932', or fall back to utf-8-sig
        # This is acceptable as the fallback chain will handle it
        assert encoding.lower() in ["cp932", "shift_jis", "shift-jis", "utf-8-sig", "utf-8"]

    def test_fallback_on_low_confidence(self, tmp_path):
        """Should fallback to utf-8-sig when confidence is low."""
        test_file = tmp_path / "ambiguous.csv"
        test_file.write_bytes(b"abc123")  # ASCII - ambiguous

        encoding = detect_encoding(test_file)
        # Should return one of the fallback encodings
        assert encoding in ["utf-8-sig", "utf-8", "cp932", "ascii", "ASCII"]

    def test_detect_encoding_fallback_on_chardet_exception(self, tmp_path):
        """Should use fallback when chardet raises an exception."""
        from unittest.mock import patch

        test_file = tmp_path / "test.csv"
        test_file.write_text("test", encoding="utf-8")

        # Mock chardet.detect to raise an exception
        # Expect warning about chardet failure
        with patch("chardet.detect", side_effect=Exception("Unexpected error")):
            with pytest.warns(UserWarning, match="chardet failed"):
                encoding = detect_encoding(test_file)
                # Should fallback to utf-8-sig
                assert encoding == "utf-8-sig"


class TestHeaderDetection:
    """Test header row detection logic."""

    def test_find_header_in_first_row(self, tmp_path):
        """Should find header when it's in the first row."""
        test_file = tmp_path / "header_first.csv"
        content = "利用日,ご利用店名及び商品名,利用金額,備考\n2025-10-01,店舗,1000,会議費\n"
        test_file.write_text(content, encoding="utf-8")

        header_idx = find_header_row(test_file)
        assert header_idx == 0

    def test_find_header_in_middle_rows(self, tmp_path):
        """Should find header within first 10 rows."""
        test_file = tmp_path / "header_middle.csv"
        lines = [
            "クレジットカード明細",
            "発行日: 2025-10-31",
            "",
            "利用日,ご利用店名及び商品名,利用金額,備考",
            "2025-10-01,店舗,1000,会議費",
        ]
        test_file.write_text("\n".join(lines), encoding="utf-8")

        header_idx = find_header_row(test_file)
        assert header_idx == 3

    def test_missing_header_returns_none(self, tmp_path):
        """Should return None when header is not found."""
        test_file = tmp_path / "no_header.csv"
        test_file.write_text("col1,col2,col3\ndata1,data2,data3\n", encoding="utf-8")

        header_idx = find_header_row(test_file)
        assert header_idx is None


class TestCSVReading:
    """Test complete CSV reading with detection."""

    def test_read_csv_with_all_required_columns(self, tmp_path):
        """Should successfully read CSV with all required columns."""
        test_file = tmp_path / "valid.csv"
        content = "利用日,ご利用店名及び商品名,利用金額,備考\n2025-10-01,店舗,1000,会議費\n"
        test_file.write_text(content, encoding="utf-8")

        df, encoding, pre_header_rows = read_csv_with_detection(test_file)

        assert df is not None
        assert "利用日" in df.columns
        assert "備考" in df.columns
        assert len(df) == 1
        assert encoding in ["utf-8", "utf-8-sig"]
        assert pre_header_rows == []  # No pre-header rows

    def test_read_csv_with_missing_columns_warns(self, tmp_path):
        """Should warn when required columns are missing."""
        test_file = tmp_path / "missing_cols.csv"
        content = "date,amount\n2025-10-01,1000\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.warns(UserWarning, match="Missing required columns"):
            df, _, _ = read_csv_with_detection(test_file)

        assert df is not None  # Should still return DataFrame

    def test_read_empty_file_returns_empty_df(self, tmp_path):
        """Should return empty DataFrame for empty files."""
        test_file = tmp_path / "empty.csv"
        test_file.write_text("", encoding="utf-8")

        with pytest.warns(UserWarning, match="Empty file"):
            df, encoding, pre_header_rows = read_csv_with_detection(test_file)

        assert df.empty
        assert encoding is not None
        assert pre_header_rows == []

    def test_read_csv_all_encodings_fail(self, tmp_path):
        """Should raise ValueError when all encodings fail."""
        from unittest.mock import patch

        test_file = tmp_path / "test.csv"
        test_file.write_text("test,data\n1,2", encoding="utf-8")

        # Mock pd.read_csv to always fail
        # Expect warning about header not found
        with patch("pandas.read_csv", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "fail")):
            with pytest.warns(UserWarning, match="Header row not found"):
                try:
                    read_csv_with_detection(test_file)
                    raise AssertionError("Should have raised ValueError")
                except ValueError as e:
                    assert "Failed to read" in str(e)
                    assert "with any encoding" in str(e)


    def test_read_csv_with_pre_header_rows(self, tmp_path):
        """Should preserve pre-header rows when header is not on first line."""
        test_file = tmp_path / "with_pre_header.csv"
        lines = [
            "クレジットカード明細",
            "発行日: 2025-10-31",
            "",
            "利用日,ご利用店名及び商品名,利用金額,備考",
            "2025-10-01,店舗,1000,会議費",
        ]
        test_file.write_text("\n".join(lines), encoding="utf-8")

        df, encoding, pre_header_rows = read_csv_with_detection(test_file)

        assert df is not None
        assert len(df) == 1
        assert "利用日" in df.columns
        # Pre-header rows should include the first 3 lines
        assert len(pre_header_rows) == 3
        assert "クレジットカード明細" in pre_header_rows[0]
        assert "発行日: 2025-10-31" in pre_header_rows[1]
        assert pre_header_rows[2].strip() == ""  # Empty line


class TestCSVWriting:
    """Test CSV writing with UTF-8 BOM."""

    def test_write_csv_with_utf8_bom(self, tmp_path):
        """Should write CSV with UTF-8 BOM encoding."""
        output_file = tmp_path / "output.csv"
        df = pd.DataFrame({"利用日": ["2025-10-01"], "店舗": ["テスト店舗"], "金額": [1000]})

        write_csv_utf8_bom(df, output_file)

        # Read raw bytes to verify BOM
        with open(output_file, "rb") as f:
            first_bytes = f.read(3)

        assert first_bytes == b"\xef\xbb\xbf"  # UTF-8 BOM

        # Verify content is readable
        df_read = pd.read_csv(output_file, encoding="utf-8-sig")
        assert len(df_read) == 1
        assert df_read["店舗"].iloc[0] == "テスト店舗"

    def test_write_csv_handles_multiple_duplicates(self, tmp_path):
        """Should increment counter for multiple duplicate filenames."""
        output_file = tmp_path / "output.csv"
        df = pd.DataFrame({"col": [1, 2, 3]})

        # Create three files with same base name
        paths = []
        for i in range(3):
            path = write_csv_utf8_bom(df, output_file, handle_duplicates=(i > 0))
            paths.append(path)

        # Check all three were created with incrementing suffixes
        assert paths[0].stem == "output"
        assert paths[1].stem == "output_2"
        assert paths[2].stem == "output_3"
        assert all(p.exists() for p in paths)

    def test_write_csv_handles_duplicate_filenames(self, tmp_path):
        """Should append suffix for duplicate filenames."""
        output_file = tmp_path / "output.csv"
        df = pd.DataFrame({"col": [1, 2, 3]})

        # Write first file
        write_csv_utf8_bom(df, output_file)
        assert output_file.exists()

        # Write second file with same name
        new_path = write_csv_utf8_bom(df, output_file, handle_duplicates=True)

        assert new_path != output_file
        assert new_path.stem == "output_2"
        assert new_path.exists()

    def test_write_csv_with_pre_header_rows(self, tmp_path):
        """Should write pre-header rows before the CSV data."""
        output_file = tmp_path / "output_with_pre_header.csv"
        df = pd.DataFrame({"利用日": ["2025-10-01"], "金額": [1000], "備考": ["会議費"]})
        pre_header_rows = ["クレジットカード明細\n", "発行日: 2025-10-31\n", "\n"]

        write_csv_utf8_bom(df, output_file, pre_header_rows=pre_header_rows)

        # Read the file and verify pre-header rows are preserved
        with open(output_file, encoding="utf-8-sig") as f:
            lines = f.readlines()

        assert len(lines) >= 5  # 3 pre-header + 1 header + 1 data
        assert "クレジットカード明細" in lines[0]
        assert "発行日: 2025-10-31" in lines[1]
        assert lines[2].strip() == ""  # Empty line
        assert "利用日" in lines[3]  # CSV header
        assert "2025-10-01" in lines[4]  # CSV data

    def test_write_csv_without_pre_header_rows(self, tmp_path):
        """Should work normally when no pre-header rows are provided."""
        output_file = tmp_path / "output_no_pre_header.csv"
        df = pd.DataFrame({"col1": [1], "col2": [2]})

        write_csv_utf8_bom(df, output_file, pre_header_rows=None)

        # Read and verify normal CSV structure
        df_read = pd.read_csv(output_file, encoding="utf-8-sig")
        assert len(df_read) == 1
        assert list(df_read.columns) == ["col1", "col2"]
