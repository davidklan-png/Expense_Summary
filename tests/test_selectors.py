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
                "科目＆No.": ["会議費", "交通費", "会議費"],
            },
        )

        result = filter_relevant_transactions(df)

        assert len(result) == 2
        assert all("会議費" in remark for remark in result["科目＆No."])

    def test_filter_entertainment_expenses(self):
        """Should filter transactions with 接待費 in remarks."""
        df = pd.DataFrame(
            {"利用日": ["2025-10-01", "2025-10-02"], "利用金額": [15000, 8000], "科目＆No.": ["接待費", "接待費"]},
        )

        result = filter_relevant_transactions(df)

        assert len(result) == 2

    def test_filter_mixed_expenses(self):
        """Should filter both 会議費 and 接待費."""
        df = pd.DataFrame(
            {
                "利用日": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04"],
                "利用金額": [10000, 5000, 3000, 8000],
                "科目＆No.": ["会議費", "交通費", "接待費", "その他"],
            },
        )

        result = filter_relevant_transactions(df)

        assert len(result) == 2
        assert result["科目＆No."].iloc[0] == "会議費"
        assert result["科目＆No."].iloc[1] == "接待費"

    def test_filter_empty_returns_empty(self):
        """Should return empty DataFrame when no matches."""
        df = pd.DataFrame({"利用日": ["2025-10-01"], "利用金額": [1000], "科目＆No.": ["その他"]})

        result = filter_relevant_transactions(df)

        assert len(result) == 0


class TestAttendeeEstimation:
    """Test attendee count estimation logic."""

    def test_estimate_within_bounds(self):
        """Should return count between min and max."""
        import random

        random.seed(42)  # Make test deterministic

        for _ in range(20):  # Test randomness with multiple runs
            count = estimate_attendee_count(amount=10000, min_attendees=2, max_attendees=8)
            assert 2 <= count <= 8

    def test_estimate_respects_minimum(self):
        """Should never return less than minimum."""
        import random

        random.seed(42)  # Make test deterministic

        for _ in range(20):
            count = estimate_attendee_count(amount=100, min_attendees=3, max_attendees=5)
            assert count >= 3

    def test_estimate_respects_maximum(self):
        """Should never return more than maximum."""
        import random

        random.seed(42)  # Make test deterministic

        for _ in range(20):
            count = estimate_attendee_count(amount=100000, min_attendees=2, max_attendees=6)
            assert count <= 6

    def test_estimate_default_range(self):
        """Should use default range 2-8 when not specified."""
        import random

        random.seed(42)  # Make test deterministic

        count = estimate_attendee_count(amount=5000)
        assert 2 <= count <= 8


class TestAttendeeIDSampling:
    """Test attendee ID selection logic."""

    def test_sample_includes_weighted_primary_ids(self):
        """Should include ID '2' (90% weight) or ID '1' (10% weight) as primary."""
        import random

        random.seed(42)  # Make test deterministic

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

    def test_sample_zero_count(self):
        """Should return all empty strings when count is 0."""
        available_ids = ["1", "2", "3"]

        ids = sample_attendee_ids(count=0, available_ids=available_ids)

        assert len(ids) == 8
        assert all(id_str == "" for id_str in ids)

    def test_sample_negative_count(self):
        """Should return all empty strings when count is negative."""
        available_ids = ["1", "2", "3"]

        ids = sample_attendee_ids(count=-1, available_ids=available_ids)

        assert len(ids) == 8
        assert all(id_str == "" for id_str in ids)

    def test_sample_no_weighted_ids(self):
        """Should sample randomly when neither ID '1' nor '2' available."""
        available_ids = ["3", "4", "5", "6"]

        ids = sample_attendee_ids(count=3, available_ids=available_ids, id_1_weight=0.1, id_2_weight=0.9)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 3
        # Should only contain IDs from available pool
        assert all(id_str in available_ids for id_str in non_empty)


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


class TestAmountBasedEstimation:
    """Test amount-based attendee estimation with brackets."""

    def test_bracket_matching_returns_within_range(self):
        """Should return attendee count within bracket's min/max range."""
        brackets = {
            (0, 5000): {"min": 2, "max": 3},
            (5001, 15000): {"min": 3, "max": 5},
        }

        # Test multiple times to verify randomness within range
        for _ in range(10):
            count = estimate_attendee_count(amount=3000, amount_brackets=brackets)
            assert 2 <= count <= 3

            count = estimate_attendee_count(amount=10000, amount_brackets=brackets)
            assert 3 <= count <= 5

    def test_no_bracket_match_uses_fallback(self):
        """Should use cost-per-person fallback when no bracket matches."""
        brackets = {
            (0, 5000): {"min": 2, "max": 3},
            (5001, 15000): {"min": 3, "max": 5},
        }

        # Amount outside all brackets: 50,000 yen
        # With default cost_per_person=3000: 50000/3000 = 16.6 -> 16 attendees
        count = estimate_attendee_count(amount=50000, amount_brackets=brackets, cost_per_person=3000, max_attendees=8)

        # Should be capped at max_attendees
        assert count == 8

    def test_fallback_minimum_two_attendees(self):
        """Should return minimum 2 attendees in fallback mode."""
        brackets = {
            (10000, 999999): {"min": 5, "max": 8},
        }

        # Small amount (1000 yen) / 3000 = 0.33 -> should return 2 (minimum)
        count = estimate_attendee_count(amount=1000, amount_brackets=brackets, cost_per_person=3000)

        assert count >= 2

    def test_no_brackets_uses_uniform_random(self):
        """Should use uniform random when brackets not configured."""
        # Test multiple times to ensure it stays within bounds
        for _ in range(10):
            count = estimate_attendee_count(
                amount=10000,
                min_attendees=2,
                max_attendees=8,
                amount_brackets=None,  # No brackets = backward compatible mode
            )
            assert 2 <= count <= 8

    def test_custom_cost_per_person(self):
        """Should use custom cost-per-person in fallback calculation."""
        brackets = {
            (0, 5000): {"min": 2, "max": 3},
        }

        # Amount outside bracket: 20,000 yen
        # With cost_per_person=5000: 20000/5000 = 4 attendees
        count = estimate_attendee_count(amount=20000, amount_brackets=brackets, cost_per_person=5000, max_attendees=8)

        assert count == 4

    def test_bracket_edge_cases(self):
        """Should match brackets at boundary values."""
        brackets = {
            (0, 5000): {"min": 2, "max": 3},
            (5001, 15000): {"min": 3, "max": 5},
        }

        # Test boundary values
        count_lower = estimate_attendee_count(amount=0, amount_brackets=brackets)
        assert 2 <= count_lower <= 3

        count_upper = estimate_attendee_count(amount=5000, amount_brackets=brackets)
        assert 2 <= count_upper <= 3

        count_next = estimate_attendee_count(amount=5001, amount_brackets=brackets)
        assert 3 <= count_next <= 5


class TestHybridCoreMemberSelection:
    """Test hybrid weighted-primary + core-member filling algorithm."""

    def test_weighted_primary_then_core_filling(self):
        """Should select primary using weights (90% ID '2'), then fill from core."""
        import random

        random.seed(42)  # Make test deterministic

        available_ids = ["1", "2", "3", "4", "5", "6"]
        core_ids = ["3", "4", "5", "6"]

        # Request 4 attendees: 1 weighted primary + 3 from core
        ids = sample_attendee_ids(count=4, available_ids=available_ids, core_ids=core_ids)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 4
        # First ID should be from weighted selection (1 or 2)
        assert non_empty[0] in ["1", "2"]
        # Remaining should be from core (excluding primary if it's core)
        remaining = non_empty[1:]
        assert all(id_str in core_ids for id_str in remaining if id_str not in ["1", "2"])

    def test_weighted_primary_is_id2_90_percent(self):
        """Should select ID '2' as primary ~90% of the time."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4"]
        core_ids = ["3", "4"]

        id_2_as_primary = 0
        trials = 100

        for _ in range(trials):
            ids = sample_attendee_ids(count=2, available_ids=available_ids, core_ids=core_ids)
            non_empty = [id_str for id_str in ids if id_str]
            if non_empty and non_empty[0] == "2":
                id_2_as_primary += 1

        # ID '2' should be primary ~90% of the time
        assert id_2_as_primary >= 80  # Allow some variance

    def test_core_exhaustion_uses_non_core(self):
        """Should use non-core members when core exhausted."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]
        core_ids = ["3", "4"]  # Only 2 core members

        # Request 5 attendees: 1 weighted primary + 1 core + 3 non-core
        ids = sample_attendee_ids(count=5, available_ids=available_ids, core_ids=core_ids)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 5

    def test_sequential_core_filling(self):
        """Should use core members in ID order when sequential strategy."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5", "6", "7", "8"]
        core_ids = ["3", "4", "5", "6", "7"]

        ids = sample_attendee_ids(
            count=4,
            available_ids=available_ids,
            core_ids=core_ids,
            core_fill_strategy="sequential",
        )

        non_empty = [id_str for id_str in ids if id_str]
        # First ID is from weighted (1 or 2)
        # Remaining 3 from core in sequential order
        remaining = non_empty[1:]
        assert remaining == sorted(remaining, key=int)

    def test_no_core_ids_uses_legacy_filling(self):
        """Should use legacy random filling when core_ids is None."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5"]

        ids = sample_attendee_ids(count=3, available_ids=available_ids, core_ids=None)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 3

    def test_empty_core_ids_uses_legacy_filling(self):
        """Should use legacy random filling when core_ids is empty."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5"]

        ids = sample_attendee_ids(count=3, available_ids=available_ids, core_ids=[])

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 3

    def test_dict_output_with_core_members(self):
        """Should return dict format with hybrid selection."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5"]
        core_ids = ["3", "4", "5"]

        result = sample_attendee_ids(count=3, available_ids=available_ids, core_ids=core_ids, return_dict=True)

        assert isinstance(result, dict)
        assert set(result.keys()) == {f"ID{i}" for i in range(1, 9)}
        # Check that we have 3 populated IDs
        populated = [v for v in result.values() if v]
        assert len(populated) == 3

    def test_backward_compatibility_without_core_ids(self):
        """Should work exactly as before when core_ids not provided."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5"]

        # Call without core_ids parameter (backward compatible)
        ids = sample_attendee_ids(count=3, available_ids=available_ids, id_2_weight=0.9, id_1_weight=0.1)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 3
        # First ID should be weighted (1 or 2)
        assert non_empty[0] in ["1", "2"]

    def test_primary_id_excluded_from_core_selection(self):
        """Should not include primary ID in core selection (avoid duplicates)."""
        import random

        random.seed(42)

        available_ids = ["1", "2", "3", "4", "5"]
        core_ids = ["1", "2", "3"]  # Core includes the weighted IDs

        ids = sample_attendee_ids(count=4, available_ids=available_ids, core_ids=core_ids)

        non_empty = [id_str for id_str in ids if id_str]
        assert len(non_empty) == 4
        # No duplicates allowed
        assert len(non_empty) == len(set(non_empty))
