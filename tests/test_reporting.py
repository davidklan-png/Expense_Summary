"""Tests for HTML report generation."""

import pandas as pd
import pytest
from saisonxform.reporting import generate_html_report, get_unique_attendees, prepare_report_context


@pytest.fixture
def sample_transactions():
    """Sample transaction DataFrame with attendee columns."""
    return pd.DataFrame(
        {
            "利用日": ["2025-10-01", "2025-10-02", "2025-10-03"],
            "ご利用店名及び商品名": ["東京レストラン", "カフェABC", "ホテル会議室"],
            "利用金額": [15000, 5000, 25000],
            "備考": ["会議費", "接待費", "会議費"],
            "出席者": [4, 2, 6],
            "ID1": ["1", "2", "1"],
            "ID2": ["2", "3", "2"],
            "ID3": ["3", "", "3"],
            "ID4": ["5", "", "4"],
            "ID5": ["", "", "5"],
            "ID6": ["", "", "7"],
            "ID7": ["", "", ""],
            "ID8": ["", "", ""],
        },
    )


@pytest.fixture
def attendee_reference():
    """Sample attendee reference DataFrame."""
    return pd.DataFrame(
        {
            "ID": ["1", "2", "3", "4", "5", "7"],
            "Name": ["山田太郎", "佐藤花子", "鈴木一郎", "田中美咲", "高橋健太", "伊藤誠"],
            "Title": ["部長", "課長", "主任", "係長", "社員", "社員"],
            "Company": ["ABC株式会社", "XYZ株式会社", "DEF株式会社", "GHI株式会社", "JKL株式会社", "MNO株式会社"],
        },
    )


class TestUniqueAttendeeExtraction:
    """Test extraction of unique attendees from transactions."""

    def test_get_unique_attendees_basic(self, sample_transactions, attendee_reference):
        """Should extract all unique attendee IDs and join with reference."""
        unique = get_unique_attendees(sample_transactions, attendee_reference)

        # Should have unique IDs: 1, 2, 3, 4, 5, 7
        assert len(unique) == 6
        assert "1" in unique["ID"].values
        assert "7" in unique["ID"].values

    def test_get_unique_attendees_sorted(self, sample_transactions, attendee_reference):
        """Should return attendees sorted by ID numerically."""
        unique = get_unique_attendees(sample_transactions, attendee_reference)

        # Convert IDs to integers for comparison
        id_values = [int(id_str) for id_str in unique["ID"]]
        assert id_values == sorted(id_values)

    def test_get_unique_attendees_empty_transactions(self, attendee_reference):
        """Should return empty DataFrame for empty transactions."""
        empty_df = pd.DataFrame(
            {"ID1": [], "ID2": [], "ID3": [], "ID4": [], "ID5": [], "ID6": [], "ID7": [], "ID8": []},
        )

        unique = get_unique_attendees(empty_df, attendee_reference)

        assert len(unique) == 0

    def test_get_unique_attendees_missing_reference(self, sample_transactions):
        """Should handle case where some IDs are not in reference."""
        partial_ref = pd.DataFrame(
            {"ID": ["1", "2"], "Name": ["山田太郎", "佐藤花子"], "Title": ["部長", "課長"], "Company": ["ABC株式会社", "XYZ株式会社"]},
        )

        unique = get_unique_attendees(sample_transactions, partial_ref)

        # Should return all unique IDs, with NaN for missing reference data
        assert len(unique) == 6  # All unique IDs from transactions
        assert "1" in unique["ID"].values
        assert "2" in unique["ID"].values
        # IDs not in reference will have NaN values for Name/Title/Company
        missing_ids = unique[unique["Name"].isna()]
        assert len(missing_ids) == 4  # 3, 4, 5, 7 not in partial reference


class TestReportContextPreparation:
    """Test preparation of context data for template rendering."""

    def test_prepare_context_structure(self, sample_transactions, attendee_reference):
        """Should create context with all required keys."""
        context = prepare_report_context(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            filename="202510_A.csv",
        )

        assert "filename" in context
        assert "transactions" in context
        assert "unique_attendees" in context
        assert "total_transactions" in context
        assert "total_amount" in context

    def test_prepare_context_metadata(self, sample_transactions, attendee_reference):
        """Should include correct metadata."""
        context = prepare_report_context(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            filename="202510_A.csv",
        )

        assert context["filename"] == "202510_A.csv"
        assert context["total_transactions"] == 3
        assert context["total_amount"] == 45000  # 15000 + 5000 + 25000

    def test_prepare_context_transactions_as_dicts(self, sample_transactions, attendee_reference):
        """Should convert transactions DataFrame to list of dicts."""
        context = prepare_report_context(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            filename="test.csv",
        )

        assert isinstance(context["transactions"], list)
        assert len(context["transactions"]) == 3
        assert isinstance(context["transactions"][0], dict)
        assert "利用日" in context["transactions"][0]

    def test_prepare_context_unique_attendees_as_dicts(self, sample_transactions, attendee_reference):
        """Should convert unique attendees to list of dicts."""
        context = prepare_report_context(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            filename="test.csv",
        )

        assert isinstance(context["unique_attendees"], list)
        assert len(context["unique_attendees"]) > 0
        assert isinstance(context["unique_attendees"][0], dict)
        assert "Name" in context["unique_attendees"][0]


class TestHTMLReportGeneration:
    """Test complete HTML report generation."""

    def test_generate_html_creates_file(self, tmp_path, sample_transactions, attendee_reference):
        """Should create HTML file at specified path."""
        output_file = tmp_path / "report.html"

        generate_html_report(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="test.csv",
        )

        assert output_file.exists()

    def test_generate_html_contains_transaction_data(self, tmp_path, sample_transactions, attendee_reference):
        """Should include transaction data in HTML."""
        output_file = tmp_path / "report.html"

        generate_html_report(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="test.csv",
        )

        content = output_file.read_text(encoding="utf-8")

        # Check for transaction details
        assert "東京レストラン" in content
        assert "カフェABC" in content
        assert "15000" in content or "15,000" in content

    def test_generate_html_contains_attendee_list(self, tmp_path, sample_transactions, attendee_reference):
        """Should include unique attendee list in HTML."""
        output_file = tmp_path / "report.html"

        generate_html_report(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="test.csv",
        )

        content = output_file.read_text(encoding="utf-8")

        # Check for attendee details
        assert "山田太郎" in content
        assert "佐藤花子" in content

    def test_generate_html_handles_duplicate_filenames(self, tmp_path, sample_transactions, attendee_reference):
        """Should append suffix for duplicate filenames."""
        output_file = tmp_path / "report.html"

        # Generate first report
        path1 = generate_html_report(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="test.csv",
        )

        # Generate second report with same filename
        path2 = generate_html_report(
            transactions=sample_transactions,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="test.csv",
            handle_duplicates=True,
        )

        assert path1 != path2
        assert path2.stem == "report_2"
        assert path1.exists()
        assert path2.exists()

    def test_generate_html_handles_multiple_duplicates(self, tmp_path, sample_transactions, attendee_reference):
        """Should increment counter for multiple duplicate filenames."""
        output_file = tmp_path / "report.html"

        # Generate three reports with same base filename
        paths = []
        for i in range(3):
            path = generate_html_report(
                transactions=sample_transactions,
                attendee_reference=attendee_reference,
                output_path=output_file,
                source_filename="test.csv",
                handle_duplicates=(i > 0),  # First one doesn't need handle_duplicates
            )
            paths.append(path)

        # Check all three were created with incrementing suffixes
        assert paths[0].stem == "report"
        assert paths[1].stem == "report_2"
        assert paths[2].stem == "report_3"
        assert all(p.exists() for p in paths)

    def test_generate_html_with_empty_transactions(self, tmp_path, attendee_reference):
        """Should handle empty transactions gracefully."""
        empty_df = pd.DataFrame(
            {
                "利用日": [],
                "ご利用店名及び商品名": [],
                "利用金額": [],
                "備考": [],
                "出席者": [],
                "ID1": [],
                "ID2": [],
                "ID3": [],
                "ID4": [],
                "ID5": [],
                "ID6": [],
                "ID7": [],
                "ID8": [],
            },
        )

        output_file = tmp_path / "empty_report.html"

        generate_html_report(
            transactions=empty_df,
            attendee_reference=attendee_reference,
            output_path=output_file,
            source_filename="empty.csv",
        )

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "empty.csv" in content or "Empty" in content or "0" in content
