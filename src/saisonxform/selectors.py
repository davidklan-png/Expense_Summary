"""Attendee estimation and ID selection logic."""
import random

import pandas as pd


def _numeric_sort_key(id_value: str) -> int | float:
    """Convert ID to numeric sort key, placing non-numeric IDs at end.

    Args:
        id_value: ID string value

    Returns:
        Integer value for numeric IDs, infinity for non-numeric
    """
    return int(id_value) if id_value.isdigit() else float("inf")


def filter_relevant_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter transactions to only meeting and entertainment expenses.

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame containing only rows where '科目＆No.' contains '会議費' or '接待費'
    """
    if "科目＆No." not in df.columns:
        return pd.DataFrame()

    # Filter for meeting expenses (会議費) or entertainment expenses (接待費)
    mask = df["科目＆No."].str.contains("会議費|接待費", na=False, regex=True)

    return df[mask].copy()


def estimate_attendee_count(
    amount: float,
    min_attendees: int = 2,
    max_attendees: int = 8,
    amount_brackets: dict[tuple[int, int], dict[str, int]] | None = None,
    cost_per_person: int = 3000,
) -> int:
    """
    Estimate number of attendees for a transaction.

    Supports three modes:
    1. Amount-based brackets: Match amount to bracket, randomly select within bracket's min/max
    2. Fallback calculation: amount / cost_per_person (minimum 2)
    3. Uniform random: Between min_attendees and max_attendees (backward compatible)

    Args:
        amount: Transaction amount in yen
        min_attendees: Minimum possible attendees for uniform random mode (default: 2)
        max_attendees: Maximum possible attendees for uniform random mode (default: 8)
        amount_brackets: Optional dict mapping (min_amount, max_amount) to {min, max} attendees
        cost_per_person: Fallback cost per person in yen (default: 3000)

    Returns:
        Estimated attendee count
    """
    # Mode 1: Amount-based brackets (if provided)
    if amount_brackets:
        for (bracket_min, bracket_max), attendee_range in amount_brackets.items():
            if bracket_min <= amount <= bracket_max:
                # Found matching bracket - randomly select within range
                return random.randint(attendee_range["min"], attendee_range["max"])

        # No bracket matched - use fallback calculation (Mode 2)
        calculated = max(2, int(amount / cost_per_person))
        # Cap at max_attendees to avoid unrealistic values
        return min(calculated, max_attendees)

    # Mode 3: Uniform random distribution (backward compatible, no amount config)
    return random.randint(min_attendees, max_attendees)


def sample_attendee_ids(
    count: int,
    available_ids: list[str],
    core_ids: list[str] | None = None,
    core_fill_strategy: str = "random",
    id_2_weight: float = 0.9,
    id_1_weight: float = 0.1,
    return_dict: bool = False,
) -> list[str] | dict[str, str]:
    """Sample attendee IDs with hybrid weighted-primary and core-member filling.

    Hybrid Algorithm (when core_ids provided):
    1. Select FIRST ID using weighted random (90% ID '2', 10% ID '1') - legacy behavior
    2. Fill remaining slots from core members (excluding the primary ID)
    3. If core members exhausted, fill from non-core available_ids
    4. Sort IDs numerically
    5. Pad to 8 slots with empty strings

    Legacy Algorithm (when core_ids is None or empty):
    1. Select primary ID using weighted random (90% ID '2', 10% ID '1')
    2. Fill remaining slots by sampling from all available IDs
    3. Sort IDs numerically
    4. Pad to 8 slots with empty strings

    Args:
        count: Number of attendees to select
        available_ids: List of all available attendee ID strings
        core_ids: Optional list of core member IDs (used after primary selection)
        core_fill_strategy: "random" (default) or "sequential" for core selection
        id_2_weight: Probability weight for ID '2' (default: 0.9)
        id_1_weight: Probability weight for ID '1' (default: 0.1)
        return_dict: If True, return dict with ID1-ID8 keys; if False, return list

    Returns:
        List of selected ID strings (padded to 8), or dict mapping ID1-ID8 to values
    """
    if count <= 0:
        selected_ids = []
    else:
        # Step 1: Select PRIMARY ID using weighted random (legacy behavior - 90% ID "2", 10% ID "1")
        primary_candidates = []
        weights = []

        if "2" in available_ids:
            primary_candidates.append("2")
            weights.append(id_2_weight)

        if "1" in available_ids:
            primary_candidates.append("1")
            weights.append(id_1_weight)

        if primary_candidates:
            # Normalize weights
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]

            # Weighted random choice for FIRST ID
            primary_id = random.choices(primary_candidates, weights=normalized_weights, k=1)[0]
            selected_ids = [primary_id]

            # Step 2: Fill remaining slots
            remaining_count = count - 1

            if remaining_count > 0:
                # Determine pool for remaining slots
                if core_ids is not None and len(core_ids) > 0:
                    # Hybrid Mode: Use core members for remaining slots
                    valid_core_ids = [id_str for id_str in core_ids if id_str in available_ids and id_str != primary_id]

                    if core_fill_strategy == "sequential":
                        # Use core IDs in order
                        selected_from_core = valid_core_ids[:remaining_count]
                    else:
                        # Random: Shuffle core IDs and take first `remaining_count`
                        shuffled_core = valid_core_ids.copy()
                        random.shuffle(shuffled_core)
                        selected_from_core = shuffled_core[:remaining_count]

                    # Add core members (excluding primary)
                    selected_ids.extend(selected_from_core)

                    # If still need more, use non-core members
                    if len(selected_ids) < count:
                        non_core_ids = [id_str for id_str in available_ids if id_str not in set(valid_core_ids) and id_str != primary_id]
                        additional_needed = count - len(selected_ids)
                        sample_count = min(additional_needed, len(non_core_ids))
                        if sample_count > 0:
                            additional_ids = random.sample(non_core_ids, sample_count)
                            selected_ids.extend(additional_ids)
                else:
                    # Legacy Mode: No core members defined - sample from all remaining
                    remaining_pool = [id_str for id_str in available_ids if id_str != primary_id]
                    sample_count = min(remaining_count, len(remaining_pool))
                    if sample_count > 0:
                        additional_ids = random.sample(remaining_pool, sample_count)
                        selected_ids.extend(additional_ids)
        else:
            # No weighted IDs ("1" or "2") available - sample from all
            sample_count = min(count, len(available_ids))
            selected_ids = random.sample(available_ids, sample_count) if sample_count > 0 else []

    # Sort numerically
    selected_ids.sort(key=_numeric_sort_key)

    # Pad to 8 slots
    padded_ids = selected_ids + [""] * (8 - len(selected_ids))
    padded_ids = padded_ids[:8]  # Ensure exactly 8 elements

    if return_dict:
        # Return as dictionary with ID1-ID8 keys
        return {f"ID{i+1}": padded_ids[i] for i in range(8)}
    else:
        return padded_ids
