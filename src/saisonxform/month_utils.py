"""Utilities for month-based file filtering and archival detection.

This module provides functions for:
- Parsing YYYYMM month prefixes from filenames
- Finding the latest N months from available files
- Detecting already-archived months
"""

import re
from pathlib import Path
from typing import Optional


def get_month_from_filename(filename: str) -> Optional[str]:
    """Extract YYYYMM month prefix from filename.

    Args:
        filename: Filename to parse (e.g., "202510_transactions.csv")

    Returns:
        YYYYMM string if found, None otherwise

    Examples:
        >>> get_month_from_filename("202510_transactions.csv")
        "202510"
        >>> get_month_from_filename("202511_data.csv")
        "202511"
        >>> get_month_from_filename("no_month_prefix.csv")
        None
    """
    # Match YYYYMM pattern at start of filename (before extension)
    match = re.match(r"^(\d{6})_", filename)
    if match:
        month_str = match.group(1)
        # Basic validation: year should be 20xx or 19xx, month 01-12
        year = int(month_str[:4])
        month = int(month_str[4:6])
        if 1900 <= year <= 2100 and 1 <= month <= 12:
            return month_str
    return None


def get_latest_months(input_dir: Path, n: int = 2) -> list[str]:
    """Find the latest N months from CSV files in input directory.

    Args:
        input_dir: Directory containing CSV files with YYYYMM prefixes
        n: Number of latest months to return (default: 2)

    Returns:
        List of YYYYMM strings, sorted in descending order (latest first)
        Returns empty list if no files with month prefixes found

    Examples:
        >>> # With files: 202510_a.csv, 202511_b.csv, 202509_c.csv
        >>> get_latest_months(Path("Input"), n=2)
        ["202511", "202510"]
    """
    if not input_dir.exists():
        return []

    # Extract unique months from all CSV files
    months: set[str] = set()
    for csv_file in input_dir.glob("*.csv"):
        month = get_month_from_filename(csv_file.name)
        if month:
            months.add(month)

    # Sort in descending order (latest first) and take top N
    sorted_months = sorted(months, reverse=True)
    return sorted_months[:n]


def get_archived_months(archive_dir: Path) -> set[str]:
    """Find all months that have been archived.

    A month is considered archived if Archive/YYYYMM/ directory exists
    (regardless of retry markers).

    Args:
        archive_dir: Archive directory path

    Returns:
        Set of YYYYMM strings for archived months

    Examples:
        >>> # With Archive/202510/ and Archive/202511/ directories
        >>> get_archived_months(Path("Archive"))
        {"202510", "202511"}
    """
    if not archive_dir.exists():
        return set()

    archived_months: set[str] = set()
    for item in archive_dir.iterdir():
        if item.is_dir():
            # Check if directory name is valid YYYYMM format
            dir_name = item.name
            if re.match(r"^\d{6}$", dir_name):
                year = int(dir_name[:4])
                month = int(dir_name[4:6])
                if 1900 <= year <= 2100 and 1 <= month <= 12:
                    archived_months.add(dir_name)

    return archived_months


def has_retry_marker(archive_dir: Path, month: str) -> bool:
    """Check if a retry marker exists for a given month.

    Args:
        archive_dir: Archive directory path
        month: YYYYMM string

    Returns:
        True if .retry_YYYYMM.json exists, False otherwise

    Examples:
        >>> has_retry_marker(Path("Archive"), "202510")
        False  # No retry marker
        >>> has_retry_marker(Path("Archive"), "202511")
        True   # .retry_202511.json exists
    """
    if not archive_dir.exists():
        return False

    retry_marker = archive_dir / f".retry_{month}.json"
    return retry_marker.exists()


def filter_files_by_months(csv_files: list[Path], months: list[str]) -> list[Path]:
    """Filter CSV files to only those matching specified months.

    Args:
        csv_files: List of CSV file paths
        months: List of YYYYMM strings to filter by

    Returns:
        Filtered list of CSV files matching any of the specified months

    Examples:
        >>> files = [Path("202510_a.csv"), Path("202511_b.csv"), Path("202509_c.csv")]
        >>> filter_files_by_months(files, ["202510", "202511"])
        [Path("202510_a.csv"), Path("202511_b.csv")]
    """
    if not months:
        return csv_files

    months_set = set(months)
    filtered = []
    for csv_file in csv_files:
        month = get_month_from_filename(csv_file.name)
        if month and month in months_set:
            filtered.append(csv_file)

    return filtered
