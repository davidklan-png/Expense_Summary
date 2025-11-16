"""Attendee estimation and ID selection logic."""
import random
from typing import Union

import pandas as pd


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
    id_2_weight: float = 0.9,
    id_1_weight: float = 0.1,
    return_dict: bool = False,
) -> Union[list[str], dict[str, str]]:
    """
    Sample attendee IDs with weighted primary selection.

    Algorithm:
    1. Select primary ID using weighted random (90% ID '2', 10% ID '1')
    2. Fill remaining slots by sampling without replacement from available IDs
    3. Sort IDs numerically
    4. Pad to 8 slots with empty strings

    Args:
        count: Number of attendees to select
        available_ids: List of available attendee ID strings
        id_2_weight: Probability weight for ID '2' (default: 0.9)
        id_1_weight: Probability weight for ID '1' (default: 0.1)
        return_dict: If True, return dict with ID1-ID8 keys; if False, return list

    Returns:
        List of selected ID strings (padded to 8), or dict mapping ID1-ID8 to values
    """
    if count <= 0:
        selected_ids = []
    else:
        # Step 1: Select primary ID with weights
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

            # Weighted random choice
            primary_id = random.choices(primary_candidates, weights=normalized_weights, k=1)[0]
            selected_ids = [primary_id]

            # Step 2: Fill remaining slots
            remaining_count = count - 1
            if remaining_count > 0:
                # Remove primary ID from available pool
                remaining_pool = [id_str for id_str in available_ids if id_str != primary_id]

                # Sample without replacement
                sample_count = min(remaining_count, len(remaining_pool))
                if sample_count > 0:
                    additional_ids = random.sample(remaining_pool, sample_count)
                    selected_ids.extend(additional_ids)
        else:
            # No weighted IDs available, sample from all
            sample_count = min(count, len(available_ids))
            selected_ids = random.sample(available_ids, sample_count) if sample_count > 0 else []

    # Step 3: Sort numerically
    selected_ids.sort(key=lambda x: int(x) if x.isdigit() else float("inf"))

    # Step 4: Pad to 8 slots
    padded_ids = selected_ids + [""] * (8 - len(selected_ids))
    padded_ids = padded_ids[:8]  # Ensure exactly 8 elements

    if return_dict:
        # Return as dictionary with ID1-ID8 keys
        return {f"ID{i+1}": padded_ids[i] for i in range(8)}
    else:
        return padded_ids
