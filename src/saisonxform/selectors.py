"""Attendee estimation and ID selection logic."""
import random
from typing import Dict, List, Union

import pandas as pd


def filter_relevant_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter transactions to only meeting and entertainment expenses.

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame containing only rows where '備考' contains '会議費' or '接待費'
    """
    if '備考' not in df.columns:
        return pd.DataFrame()

    # Filter for meeting expenses (会議費) or entertainment expenses (接待費)
    mask = df['備考'].str.contains('会議費|接待費', na=False, regex=True)

    return df[mask].copy()


def estimate_attendee_count(
    amount: float,
    min_attendees: int = 2,
    max_attendees: int = 8
) -> int:
    """
    Estimate number of attendees for a transaction.

    Uses uniform random distribution between min and max bounds.
    Can be extended to use amount-based weighting if configured.

    Args:
        amount: Transaction amount in yen
        min_attendees: Minimum possible attendees (default: 2)
        max_attendees: Maximum possible attendees (default: 8)

    Returns:
        Estimated attendee count
    """
    # For now, use uniform random distribution
    # Future enhancement: Add amount-based weighting from config
    return random.randint(min_attendees, max_attendees)


def sample_attendee_ids(
    count: int,
    available_ids: List[str],
    id_2_weight: float = 0.9,
    id_1_weight: float = 0.1,
    return_dict: bool = False
) -> Union[List[str], Dict[str, str]]:
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

        if '2' in available_ids:
            primary_candidates.append('2')
            weights.append(id_2_weight)

        if '1' in available_ids:
            primary_candidates.append('1')
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
    selected_ids.sort(key=lambda x: int(x) if x.isdigit() else float('inf'))

    # Step 4: Pad to 8 slots
    padded_ids = selected_ids + [''] * (8 - len(selected_ids))
    padded_ids = padded_ids[:8]  # Ensure exactly 8 elements

    if return_dict:
        # Return as dictionary with ID1-ID8 keys
        return {f'ID{i+1}': padded_ids[i] for i in range(8)}
    else:
        return padded_ids
