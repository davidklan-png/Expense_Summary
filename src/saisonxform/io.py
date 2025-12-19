"""CSV I/O operations with encoding detection and header parsing."""
import warnings
from pathlib import Path
from typing import Optional

import chardet
import pandas as pd

# Required column names for transaction CSVs
REQUIRED_COLUMNS = ["利用日", "ご利用店名及び商品名", "利用金額", "科目＆No."]

# Column name aliases - alternative names for the same columns
COLUMN_ALIASES = {
    "科目＆No.": ["科目＆No.", "備考", "科目"],  # Category/Subject column
}

# Encoding fallback chain
ENCODING_FALLBACKS = ["utf-8-sig", "utf-8", "cp932"]

# Confidence threshold for chardet
CHARDET_CONFIDENCE_THRESHOLD = 0.6


def detect_encoding(file_path: Path) -> str:
    """
    Detect file encoding using chardet with fallback chain.

    Args:
        file_path: Path to the file to analyze

    Returns:
        Detected or fallback encoding name

    Algorithm:
        1. Use chardet to detect encoding
        2. If confidence < 0.6 or detection fails, use fallback chain
        3. Fallback order: utf-8-sig → utf-8 → cp932
    """
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()

        # Try chardet detection
        result = chardet.detect(raw_data)
        encoding = result.get("encoding")
        confidence = result.get("confidence", 0)

        if encoding and confidence >= CHARDET_CONFIDENCE_THRESHOLD:
            return encoding

        # Low confidence or no detection - use fallback
        warnings.warn(f"Low confidence ({confidence:.2f}) for {file_path.name}, " f"using fallback encoding chain")

    except Exception as e:
        warnings.warn(f"chardet failed for {file_path.name}: {e}, using fallback")

    # Return first fallback
    return ENCODING_FALLBACKS[0]


def find_header_row(file_path: Path, encoding: Optional[str] = None) -> Optional[int]:
    """
    Find the row index containing the required CSV headers.

    Scans the first 10 rows looking for a row that contains all required columns.
    Supports column name aliases (e.g., '備考' as an alias for '科目＆No.').

    Args:
        file_path: Path to the CSV file
        encoding: File encoding (auto-detected if None)

    Returns:
        Zero-based index of header row, or None if not found
    """
    if encoding is None:
        encoding = detect_encoding(file_path)

    try:
        # Try each fallback encoding if the provided one fails
        encodings_to_try = [encoding] + [e for e in ENCODING_FALLBACKS if e != encoding]

        for enc in encodings_to_try:
            try:
                with open(file_path, encoding=enc) as f:
                    for idx, line in enumerate(f):
                        if idx >= 20:  # Only scan first 20 rows
                            break

                        # Check if this line contains all required columns (or their aliases)
                        has_all_columns = True
                        for col in REQUIRED_COLUMNS:
                            # Check if column or any of its aliases are in the line
                            aliases = COLUMN_ALIASES.get(col, [col])
                            if not any(alias in line for alias in aliases):
                                has_all_columns = False
                                break

                        if has_all_columns:
                            return idx

                # Successfully read file but didn't find header
                return None

            except (UnicodeDecodeError, LookupError):
                continue

        # All encodings failed
        return None

    except Exception:
        return None


def read_csv_with_detection(file_path: Path, encoding: Optional[str] = None) -> tuple[pd.DataFrame, str, list[str]]:
    """
    Read CSV file with automatic encoding detection and header parsing.

    Args:
        file_path: Path to the CSV file
        encoding: Optional encoding override

    Returns:
        Tuple of (DataFrame, encoding_used, pre_header_rows)
        - DataFrame: The parsed data starting from header row
        - encoding_used: The encoding that successfully read the file
        - pre_header_rows: List of raw lines before the header row (empty if header is on first row)

    Warnings:
        - Issues warnings for missing columns
        - Issues warnings for empty files
        - Issues warnings for encoding issues
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Detect encoding if not provided
    if encoding is None:
        encoding = detect_encoding(file_path)

    # Find header row
    header_row = find_header_row(file_path, encoding)

    if header_row is None:
        warnings.warn(f"Header row not found in {file_path.name}, attempting default read")
        header_row = 0

    # Try reading with detected encoding, fallback through chain if needed
    encodings_to_try = [encoding] + [e for e in ENCODING_FALLBACKS if e != encoding]
    last_error = None

    for enc in encodings_to_try:
        try:
            # Check if file is empty and read all lines
            with open(file_path, encoding=enc) as f:
                all_lines = f.readlines()
                if not all_lines or not "".join(all_lines).strip():
                    warnings.warn(f"Empty file: {file_path.name}")
                    return pd.DataFrame(), enc, []

            # Extract pre-header rows (if any)
            pre_header_rows = all_lines[:header_row] if header_row > 0 else []

            # Read CSV
            df = pd.read_csv(file_path, encoding=enc, skiprows=header_row)

            # Normalize column names using aliases
            column_mapping = {}
            for required_col in REQUIRED_COLUMNS:
                if required_col not in df.columns:
                    # Check if any alias exists in the DataFrame
                    aliases = COLUMN_ALIASES.get(required_col, [])
                    for alias in aliases:
                        if alias in df.columns:
                            column_mapping[alias] = required_col
                            break

            # Apply column renaming if any aliases were found
            if column_mapping:
                df = df.rename(columns=column_mapping)

            # Check for required columns after normalization
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                warnings.warn(f"Missing required columns in {file_path.name}: {missing_cols}")

            return df, enc, pre_header_rows

        except (UnicodeDecodeError, pd.errors.EmptyDataError) as e:
            last_error = e
            continue

    # All encodings failed
    if last_error:
        raise ValueError(f"Failed to read {file_path.name} with any encoding. Last error: {last_error}")

    return pd.DataFrame(), encoding, []


def write_csv_utf8_bom(
    df: pd.DataFrame,
    file_path: Path,
    handle_duplicates: bool = False,
    pre_header_rows: Optional[list[str]] = None,
) -> Path:
    """
    Write DataFrame to CSV with UTF-8 BOM encoding, optionally including pre-header rows.

    Args:
        df: DataFrame to write
        file_path: Output file path
        handle_duplicates: If True, append numeric suffix for existing files
        pre_header_rows: Optional list of raw text lines to write before the CSV header

    Returns:
        Actual path written (may differ if handle_duplicates=True)
    """
    output_path = Path(file_path)

    # Handle duplicate filenames
    if handle_duplicates and output_path.exists():
        counter = 2
        while True:
            new_path = output_path.parent / f"{output_path.stem}_{counter}{output_path.suffix}"
            if not new_path.exists():
                output_path = new_path
                break
            counter += 1

    # Write with UTF-8 BOM
    if pre_header_rows:
        # Write pre-header rows first, then the DataFrame
        with open(output_path, "w", encoding="utf-8-sig") as f:
            # Write pre-header rows (they already include newlines from readlines())
            for line in pre_header_rows:
                f.write(line)
            # Write DataFrame CSV content
            df.to_csv(f, index=False)
    else:
        # No pre-header rows, write DataFrame directly
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path
