"""Utilities for month-based file filtering and archival detection.

This module provides functions for:
- Parsing YYYYMM month prefixes from filenames
- Finding the latest N months from available files
- Detecting already-archived months
- Archiving processed files to Archive/YYYYMM/
- Managing retry markers for failed archival
"""

import json
import re
import shutil
from datetime import datetime
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


def archive_file(file_path: Path, archive_dir: Path, month: str) -> Path:
    """Move a file to Archive/YYYYMM/ directory.

    Creates Archive/ and YYYYMM/ subdirectories if they don't exist.
    Handles cross-filesystem moves using copy+delete.

    Args:
        file_path: Source file path to archive
        archive_dir: Archive root directory
        month: YYYYMM string for subdirectory

    Returns:
        Path to archived file location

    Raises:
        FileNotFoundError: If source file doesn't exist
        PermissionError: If lacking permissions for move/delete
        OSError: For other filesystem errors

    Examples:
        >>> archive_file(Path("Input/202510_data.csv"), Path("Archive"), "202510")
        Path("Archive/202510/202510_data.csv")
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    # Create Archive/YYYYMM/ directory
    month_archive_dir = archive_dir / month
    month_archive_dir.mkdir(parents=True, exist_ok=True)

    # Destination path
    dest_path = month_archive_dir / file_path.name

    # Handle existing file at destination
    if dest_path.exists():
        # Add timestamp to avoid collision
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = dest_path.stem
        suffix = dest_path.suffix
        dest_path = month_archive_dir / f"{stem}_{timestamp}{suffix}"

    # Try move first (fast if same filesystem)
    try:
        shutil.move(str(file_path), str(dest_path))
    except (OSError, PermissionError) as e:
        # If move fails, try copy+delete (works across filesystems)
        try:
            shutil.copy2(str(file_path), str(dest_path))
            file_path.unlink()
        except Exception as copy_error:
            raise OSError(f"Failed to archive file {file_path}: {copy_error}") from e

    return dest_path


def create_retry_marker(archive_dir: Path, month: str, failed_files: list[str], errors: list[str]) -> Path:
    """Create a retry marker JSON file for a partially failed month.

    Args:
        archive_dir: Archive directory path
        month: YYYYMM string
        failed_files: List of filenames that failed to process
        errors: List of error messages corresponding to failed files

    Returns:
        Path to created retry marker file

    Examples:
        >>> create_retry_marker(
        ...     Path("Archive"),
        ...     "202510",
        ...     ["202510_a.csv", "202510_b.csv"],
        ...     ["Error 1", "Error 2"]
        ... )
        Path("Archive/.retry_202510.json")
    """
    archive_dir.mkdir(parents=True, exist_ok=True)

    retry_data = {
        "month": month,
        "failed_files": failed_files,
        "errors": errors,
        "timestamp": datetime.now().isoformat(),
    }

    retry_marker_path = archive_dir / f".retry_{month}.json"
    with open(retry_marker_path, "w", encoding="utf-8") as f:
        json.dump(retry_data, f, indent=2, ensure_ascii=False)

    return retry_marker_path


def delete_retry_marker(archive_dir: Path, month: str) -> bool:
    """Delete retry marker for a month (all files succeeded).

    Args:
        archive_dir: Archive directory path
        month: YYYYMM string

    Returns:
        True if marker was deleted, False if it didn't exist

    Examples:
        >>> delete_retry_marker(Path("Archive"), "202510")
        True  # Marker was deleted
    """
    retry_marker = archive_dir / f".retry_{month}.json"
    if retry_marker.exists():
        retry_marker.unlink()
        return True
    return False


def get_files_to_archive_by_month(processed_files: list[Path]) -> dict[str, list[Path]]:
    """Group processed files by month for batch archival.

    Args:
        processed_files: List of successfully processed file paths

    Returns:
        Dictionary mapping YYYYMM -> list of file paths

    Examples:
        >>> files = [Path("202510_a.csv"), Path("202510_b.csv"), Path("202511_c.csv")]
        >>> get_files_to_archive_by_month(files)
        {"202510": [Path("202510_a.csv"), Path("202510_b.csv")], "202511": [Path("202511_c.csv")]}
    """
    month_files: dict[str, list[Path]] = {}

    for file_path in processed_files:
        month = get_month_from_filename(file_path.name)
        if month:
            if month not in month_files:
                month_files[month] = []
            month_files[month].append(file_path)

    return month_files
