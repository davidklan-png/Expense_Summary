"""Tests for month_utils module."""

from pathlib import Path

from saisonxform.month_utils import (
    filter_files_by_months,
    get_archived_months,
    get_latest_months,
    get_month_from_filename,
    has_retry_marker,
)


class TestGetMonthFromFilename:
    """Test month extraction from filenames."""

    def test_valid_month_prefix(self):
        """Should extract YYYYMM from valid filenames."""
        assert get_month_from_filename("202510_transactions.csv") == "202510"
        assert get_month_from_filename("202511_data.csv") == "202511"
        assert get_month_from_filename("202012_report.csv") == "202012"

    def test_no_month_prefix(self):
        """Should return None for files without month prefix."""
        assert get_month_from_filename("transactions.csv") is None
        assert get_month_from_filename("data_file.csv") is None
        assert get_month_from_filename("NameList.csv") is None

    def test_invalid_month_format(self):
        """Should return None for invalid month formats."""
        assert get_month_from_filename("20251_transactions.csv") is None  # 5 digits
        assert get_month_from_filename("2025101_data.csv") is None  # 7 digits
        assert get_month_from_filename("202513_data.csv") is None  # Invalid month (13)
        assert get_month_from_filename("202500_data.csv") is None  # Invalid month (00)

    def test_future_and_past_years(self):
        """Should accept years from 1900-2100."""
        assert get_month_from_filename("190001_data.csv") == "190001"
        assert get_month_from_filename("210012_data.csv") == "210012"
        assert get_month_from_filename("189912_data.csv") is None  # Before 1900
        assert get_month_from_filename("210112_data.csv") is None  # After 2100

    def test_month_prefix_not_at_start(self):
        """Should return None if month is not at start of filename."""
        assert get_month_from_filename("data_202510_file.csv") is None
        assert get_month_from_filename("report202510.csv") is None


class TestGetLatestMonths:
    """Test finding latest N months from directory."""

    def test_latest_two_months(self, tmp_path):
        """Should return 2 latest months in descending order."""
        # Create test files
        (tmp_path / "202510_a.csv").touch()
        (tmp_path / "202511_b.csv").touch()
        (tmp_path / "202509_c.csv").touch()
        (tmp_path / "202508_d.csv").touch()

        result = get_latest_months(tmp_path, n=2)

        assert result == ["202511", "202510"]

    def test_latest_three_months(self, tmp_path):
        """Should respect n parameter."""
        (tmp_path / "202510_a.csv").touch()
        (tmp_path / "202511_b.csv").touch()
        (tmp_path / "202509_c.csv").touch()
        (tmp_path / "202508_d.csv").touch()

        result = get_latest_months(tmp_path, n=3)

        assert result == ["202511", "202510", "202509"]

    def test_no_month_prefixed_files(self, tmp_path):
        """Should return empty list if no files with month prefixes."""
        (tmp_path / "data.csv").touch()
        (tmp_path / "transactions.csv").touch()

        result = get_latest_months(tmp_path)

        assert result == []

    def test_mixed_files(self, tmp_path):
        """Should ignore files without month prefixes."""
        (tmp_path / "202510_a.csv").touch()
        (tmp_path / "202511_b.csv").touch()
        (tmp_path / "NameList.csv").touch()
        (tmp_path / "data.csv").touch()

        result = get_latest_months(tmp_path, n=2)

        assert result == ["202511", "202510"]

    def test_nonexistent_directory(self):
        """Should return empty list for nonexistent directory."""
        result = get_latest_months(Path("/nonexistent"))

        assert result == []

    def test_duplicate_months(self, tmp_path):
        """Should deduplicate months from multiple files."""
        (tmp_path / "202510_a.csv").touch()
        (tmp_path / "202510_b.csv").touch()
        (tmp_path / "202511_c.csv").touch()

        result = get_latest_months(tmp_path, n=2)

        assert result == ["202511", "202510"]


class TestGetArchivedMonths:
    """Test detection of archived months."""

    def test_archived_months(self, tmp_path):
        """Should find all YYYYMM subdirectories."""
        (tmp_path / "202510").mkdir()
        (tmp_path / "202511").mkdir()
        (tmp_path / "202509").mkdir()

        result = get_archived_months(tmp_path)

        assert result == {"202510", "202511", "202509"}

    def test_invalid_directory_names(self, tmp_path):
        """Should ignore non-YYYYMM directories."""
        (tmp_path / "202510").mkdir()
        (tmp_path / "invalid").mkdir()
        (tmp_path / "20251").mkdir()  # 5 digits
        (tmp_path / "202513").mkdir()  # Invalid month

        result = get_archived_months(tmp_path)

        assert result == {"202510"}

    def test_files_ignored(self, tmp_path):
        """Should ignore files, only consider directories."""
        (tmp_path / "202510").mkdir()
        (tmp_path / "202511.txt").touch()
        (tmp_path / ".retry_202509.json").touch()

        result = get_archived_months(tmp_path)

        assert result == {"202510"}

    def test_nonexistent_archive_dir(self):
        """Should return empty set for nonexistent directory."""
        result = get_archived_months(Path("/nonexistent"))

        assert result == set()

    def test_empty_archive_dir(self, tmp_path):
        """Should return empty set for empty directory."""
        result = get_archived_months(tmp_path)

        assert result == set()


class TestHasRetryMarker:
    """Test retry marker detection."""

    def test_retry_marker_exists(self, tmp_path):
        """Should return True if retry marker file exists."""
        (tmp_path / ".retry_202510.json").touch()

        assert has_retry_marker(tmp_path, "202510") is True

    def test_retry_marker_not_exists(self, tmp_path):
        """Should return False if retry marker doesn't exist."""
        assert has_retry_marker(tmp_path, "202510") is False

    def test_nonexistent_archive_dir(self):
        """Should return False for nonexistent directory."""
        assert has_retry_marker(Path("/nonexistent"), "202510") is False

    def test_multiple_retry_markers(self, tmp_path):
        """Should correctly identify specific month's marker."""
        (tmp_path / ".retry_202510.json").touch()
        (tmp_path / ".retry_202511.json").touch()

        assert has_retry_marker(tmp_path, "202510") is True
        assert has_retry_marker(tmp_path, "202511") is True
        assert has_retry_marker(tmp_path, "202509") is False


class TestFilterFilesByMonths:
    """Test filtering CSV files by months."""

    def test_filter_single_month(self, tmp_path):
        """Should filter to only matching month."""
        files = [
            tmp_path / "202510_a.csv",
            tmp_path / "202511_b.csv",
            tmp_path / "202509_c.csv",
        ]

        result = filter_files_by_months(files, ["202510"])

        assert result == [tmp_path / "202510_a.csv"]

    def test_filter_multiple_months(self, tmp_path):
        """Should filter to any matching month."""
        files = [
            tmp_path / "202510_a.csv",
            tmp_path / "202511_b.csv",
            tmp_path / "202509_c.csv",
            tmp_path / "202508_d.csv",
        ]

        result = filter_files_by_months(files, ["202510", "202511"])

        assert result == [
            tmp_path / "202510_a.csv",
            tmp_path / "202511_b.csv",
        ]

    def test_no_matching_files(self, tmp_path):
        """Should return empty list if no matches."""
        files = [
            tmp_path / "202510_a.csv",
            tmp_path / "202511_b.csv",
        ]

        result = filter_files_by_months(files, ["202509"])

        assert result == []

    def test_empty_months_list(self, tmp_path):
        """Should return all files if months list is empty."""
        files = [
            tmp_path / "202510_a.csv",
            tmp_path / "202511_b.csv",
        ]

        result = filter_files_by_months(files, [])

        assert result == files

    def test_files_without_month_prefix(self, tmp_path):
        """Should exclude files without month prefix."""
        files = [
            tmp_path / "202510_a.csv",
            tmp_path / "NameList.csv",
            tmp_path / "data.csv",
        ]

        result = filter_files_by_months(files, ["202510"])

        assert result == [tmp_path / "202510_a.csv"]

    def test_empty_file_list(self):
        """Should return empty list for empty input."""
        result = filter_files_by_months([], ["202510"])

        assert result == []
