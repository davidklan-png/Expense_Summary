"""CSV I/O operations with encoding detection and header parsing."""
import warnings
from pathlib import Path
from typing import Optional

import chardet
import pandas as pd

# Required column names for transaction CSVs
REQUIRED_COLUMNS = ["利用日", "ご利用店名及び商品名", "利用金額", "備考"]

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
                        if idx >= 10:  # Only scan first 10 rows
                            break

                        # Check if this line contains all required columns
                        if all(col in line for col in REQUIRED_COLUMNS):
                            return idx

                # Successfully read file but didn't find header
                return None

            except (UnicodeDecodeError, LookupError):
                continue

        # All encodings failed
        return None

    except Exception:
        return None


def read_csv_with_detection(file_path: Path, encoding: Optional[str] = None) -> tuple[pd.DataFrame, str]:
    """
    Read CSV file with automatic encoding detection and header parsing.

    Args:
        file_path: Path to the CSV file
        encoding: Optional encoding override

    Returns:
        Tuple of (DataFrame, encoding_used)

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
            # Check if file is empty
            with open(file_path, encoding=enc) as f:
                content = f.read()
                if not content.strip():
                    warnings.warn(f"Empty file: {file_path.name}")
                    return pd.DataFrame(), enc

            # Read CSV
            df = pd.read_csv(file_path, encoding=enc, skiprows=header_row)

            # Check for required columns
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                warnings.warn(f"Missing required columns in {file_path.name}: {missing_cols}")

            return df, enc

        except (UnicodeDecodeError, pd.errors.EmptyDataError) as e:
            last_error = e
            continue

    # All encodings failed
    if last_error:
        raise ValueError(f"Failed to read {file_path.name} with any encoding. Last error: {last_error}")

    return pd.DataFrame(), encoding


def write_csv_utf8_bom(df: pd.DataFrame, file_path: Path, handle_duplicates: bool = False) -> Path:
    """
    Write DataFrame to CSV with UTF-8 BOM encoding.

    Args:
        df: DataFrame to write
        file_path: Output file path
        handle_duplicates: If True, append numeric suffix for existing files

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
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path
