"""Tests for attendee estimation and ID selection logic."""
import pandas as pd
from saisonxform.selectors import estimate_attendee_count, filter_relevant_transactions, sample_attendee_ids


class TestTransactionFiltering:
    """Test filtering of meeting and entertainment expenses."""

    def test_filter_meeting_expenses(self):
        """Should filter transactions with 会議費 in remarks."""
        df = pd.DataFrame(
            {
                "利用日": ["2025-10-01", "2025-10-02", "2025-10-03"],
                "利用金額": [10000, 5000, 3000],
                "備考": ["会議費", "交通費", "会議費"],
            },
        )

        result = filter_relevant_transactions(df)

        assert len(result) == 2
        assert all("会議費" in remark for remark in result["備考"])

    def test_filter_entertainment_expenses(self):
        """Should filter transactions with 接待費 in remarks."""
        df = pd.DataFrame({"利用日": ["2025-10-01", "2025-10-02"], "利用金額": [15000, 8000], "備考": ["接待費", "接待費"]})

        result = filter_relevant_transactions(df)

        assert len(result) == 2

    def test_filter_mixed_expenses(self):
        """Should filter both 会議費 and 接待費."""
        df = pd.DataFrame(
            {
                "利用日": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04"],
                "利用金額": [10000, 5000, 3000, 8000],
                "備考": ["会議費", "交通費", "接待費", "その他"],
            },
        )

        result = filter_relevant_transactions(df)

        assert len(result) == 2
        assert result["備考"].iloc[0] == "会議費"
        assert result["備考"].iloc[1] == "接待費"

    def test_filter_empty_returns_empty(self):
        """Should return empty DataFrame when no matches."""
        df = pd.DataFrame({"利用日": ["2025-10-01"], "利用金額": [1000], "備考": ["その他"]})

        result = filter_relevant_transactions(df)

        assert len(result) == 0


class TestAttendeeEstimation:
    """Test attendee count estimation logic."""

    def test_estimate_within_bounds(self):
        """Should return count between min and max."""
        for _ in range(20):  # Test randomness with multiple runs
            count = estimate_attendee_count(amount=10000, min_attendees=2, max_attendees=8)
            assert 2 <= count <= 8

    def test_estimate_respects_minimum(self):
        """Should never return less than minimum."""
        for _ in range(20):
            count = estimate_attendee_count(amount=100, min_attendees=3, max_attendees=5)
            assert count >= 3

    def test_estimate_respects_maximum(self):
        """Should never return more than maximum."""
        for _ in range(20):
            count = estimate_attendee_count(amount=100000, min_attendees=2, max_attendees=6)
            assert count <= 6

    def test_estimate_default_range(self):
        """Should use default range 2-8 when not specified."""
        count = estimate_attendee_count(amount=5000)
        assert 2 <= count <= 8


class TestAttendeeIDSampling:
    """Test attendee ID selection logic."""

    def test_sample_includes_weighted_primary_ids(self):
        """Should include ID '2' (90% weight) or ID '1' (10% weight) as primary."""
        available_ids = ["1", "2", "3", "4", "5"]

        # Run multiple times to check distribution
        id_1_count = 0
        id_2_count = 0

        for _ in range(100):
            ids = sample_attendee_ids(count=3, available_ids=available_ids, id_2_weight=0.9, id_1_weight=0.1)

            if "2" in ids:
                id_2_count += 1
            if "1" in ids:
                id_1_count += 1

        # ID '2' should appear much more frequently (~90%)
        assert id_2_count > id_1_count
        assert id_2_count >= 75  # Should be around 90, but allow some variance

    def test_sample_returns_correct_count(self):
        """Should return list padded to 8, with correct number of non-empty IDs."""
        available_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]

        for count in range(1, 8):
            ids = sample_attendee_ids(count=count, available_ids=available_ids)
            assert len(ids) == 8  # Always padded to 8
            non_empty = [id_str for id_str in ids if id_str]
            assert len(non_empty) == count  # Correct number of populated IDs

    def test_sample_no_duplicates(self):
        """Should not return duplicate IDs among non-empty values."""
        available_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]

        ids = sample_attendee_ids(count=5, available_ids=available_ids)

        # Filter out empty strings before checking for duplicates
        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == len(set(non_empty))  # No duplicates

    def test_sample_pads_to_id8(self):
        """Should pad with empty strings up to ID8."""
        available_ids = ["1", "2", "3"]

        ids_dict = sample_attendee_ids(count=2, available_ids=available_ids, return_dict=True)

        assert len(ids_dict) == 8  # ID1 through ID8
        assert ids_dict["ID1"] != ""
        assert ids_dict["ID2"] != ""
        assert ids_dict["ID3"] == ""
        assert ids_dict["ID8"] == ""

    def test_sample_sorts_numerically(self):
        """Should sort IDs numerically."""
        available_ids = ["1", "2", "10", "3", "20"]

        ids = sample_attendee_ids(count=4, available_ids=available_ids)

        # Convert to integers for comparison
        id_values = [int(id_str) for id_str in ids if id_str]

        # Check if sorted
        assert id_values == sorted(id_values)

    def test_sample_handles_insufficient_ids(self):
        """Should handle case where fewer IDs available than requested."""
        available_ids = ["1", "2"]

        ids = sample_attendee_ids(count=5, available_ids=available_ids)

        # Should return only available IDs (2 total)
        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) <= 2


class TestIDDictionaryFormat:
    """Test ID dictionary output format."""

    def test_dict_format_has_all_keys(self):
        """Should return dictionary with ID1 through ID8 keys."""
        available_ids = ["1", "2", "3", "4", "5"]

        result = sample_attendee_ids(count=3, available_ids=available_ids, return_dict=True)

        expected_keys = [f"ID{i}" for i in range(1, 9)]
        assert list(result.keys()) == expected_keys

    def test_dict_format_sparse_attendees(self):
        """Should have empty strings for unpopulated ID slots."""
        available_ids = ["1", "2", "3"]

        result = sample_attendee_ids(count=2, available_ids=available_ids, return_dict=True)

        # Count non-empty values
        populated = sum(1 for v in result.values() if v != "")

        assert populated == 2
        assert result["ID3"] == ""
        assert result["ID8"] == ""
