# Saison Transform - Comprehensive Codebase Fix and Update Plan

**Generated**: 2026-01-23
**Codebase Version**: 0.2.3
**Coverage Target**: 91% (currently ~90%)
**Test Lines**: 3,311 lines across 8 test modules

---

## Executive Summary

This document provides a comprehensive, prioritized plan to fix issues identified in the Saison Transform codebase. Issues are categorized by severity and impact, with specific file locations and recommended fixes.

**Critical Issues**: 5 (Security & Production Bugs)
**High Priority**: 8 (Type Safety, Error Handling, Configuration)
**Medium Priority**: 12 (Code Quality, Testing, Documentation)
**Low Priority**: 7 (Optimization, Cleanup)

---

## PHASE 1: CRITICAL SECURITY & PRODUCTION FIXES (Priority: IMMEDIATE)

### 1.1 Replace Production Assertions with Proper Error Handling

**Severity**: CRITICAL
**Files**: `src/saisonxform/cli.py:337`, `web_app.py:159`

**Issue**: Assertions are stripped in optimized Python (`python -O`), causing silent failures in production.

**Current Code** (`cli.py:337`):
```python
assert isinstance(ids_result, dict)
```

**Current Code** (`web_app.py:159`):
```python
assert isinstance(ids_result, dict)
```

**Fix**:
```python
# In both files, replace assertions with explicit type checking
if not isinstance(ids_result, dict):
    raise TypeError(
        f"Expected dict from sample_attendee_ids with return_dict=True, "
        f"got {type(ids_result).__name__}"
    )
```

**Why**: Ensures type validation works in all Python execution modes.

---

### 1.2 Fix Temporary File Security Vulnerability

**Severity**: CRITICAL
**Files**: `web_app.py:102-108`

**Issue**: Predictable temp file paths in world-writable `/tmp` directory create race conditions and security risks.

**Current Code**:
```python
temp_path = Path(f"/tmp/{filename}")  # Predictable, insecure
with open(temp_path, "wb") as f:
    f.write(file_bytes)

# Process the file
df, encoding, pre_header_rows = read_csv_with_detection(temp_path)
temp_path.unlink()  # May not execute if exception occurs above
```

**Fix**:
```python
import tempfile

# Use secure temporary file with context manager
with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_file:
    tmp_file.write(file_bytes)
    temp_path = Path(tmp_file.name)

try:
    # Process the file
    df, encoding, pre_header_rows = read_csv_with_detection(temp_path)
finally:
    # Guaranteed cleanup
    temp_path.unlink(missing_ok=True)
```

**Why**:
- Uses cryptographically secure temp file creation
- Prevents race conditions
- Guarantees cleanup with try-finally

---

### 1.3 Add Path Traversal Validation

**Severity**: CRITICAL
**Files**: `src/saisonxform/config.py:168-180`

**Issue**: User-supplied paths from CLI/environment variables can escape project directory.

**Current Code**:
```python
def _resolve_path(self, path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (self.project_root / path).resolve()
```

**Fix**:
```python
def _resolve_path(self, path_str: str) -> Path:
    """Resolve and validate path to prevent directory traversal.

    Args:
        path_str: Path string (relative or absolute)

    Returns:
        Resolved absolute Path object

    Raises:
        ValueError: If resolved path escapes project root (for relative paths)
    """
    path = Path(path_str)

    if path.is_absolute():
        # Allow absolute paths but warn if outside project
        return path.resolve()

    # Resolve relative path
    resolved = (self.project_root / path).resolve()

    # Validate it doesn't escape project root (path traversal check)
    try:
        resolved.relative_to(self.project_root)
    except ValueError:
        raise ValueError(
            f"Path '{path_str}' resolves outside project root. "
            f"Resolved: {resolved}, Root: {self.project_root}"
        )

    return resolved
```

**Why**: Prevents malicious `../../` paths from accessing sensitive directories.

---

### 1.4 Fix Configuration Default Inconsistencies

**Severity**: HIGH
**Files**: `src/saisonxform/config.py:187,199,211,223` vs `pyproject.toml:37-40`

**Issue**: Default paths conflict between pyproject.toml (`data/input`) and config.py (`../Input`).

**Current Code** (`config.py:187`):
```python
return self._resolve_path(self._config.get("input_dir", "../Input"))
```

**pyproject.toml** (lines 37-40):
```toml
input_dir = "data/input"
reference_dir = "data/reference"
output_dir = "data/output"
archive_dir = "data/archive"
```

**Fix** (`config.py`):
```python
# Update all default paths to match documented structure
@property
def input_dir(self) -> Path:
    if "input_dir" in self._dir_overrides:
        return self._dir_overrides["input_dir"]
    return self._resolve_path(self._config.get("input_dir", "data/input"))

@property
def reference_dir(self) -> Path:
    if "reference_dir" in self._dir_overrides:
        return self._dir_overrides["reference_dir"]
    return self._resolve_path(self._config.get("reference_dir", "data/reference"))

@property
def output_dir(self) -> Path:
    if "output_dir" in self._dir_overrides:
        return self._dir_overrides["output_dir"]
    return self._resolve_path(self._config.get("output_dir", "data/output"))

@property
def archive_dir(self) -> Path:
    if "archive_dir" in self._dir_overrides:
        return self._dir_overrides["archive_dir"]
    return self._resolve_path(self._config.get("archive_dir", "data/archive"))
```

**Why**: Single source of truth for default paths, matches documented structure.

---

### 1.5 Add Configuration Value Validation

**Severity**: HIGH
**Files**: `src/saisonxform/config.py:54-56`

**Issue**: No validation that configuration values are logically consistent.

**Current Code**:
```python
self.min_attendees = self._config.get("min_attendees", 2)
self.max_attendees = self._config.get("max_attendees", 8)
self.primary_id_weights = self._config.get("primary_id_weights", {"2": 0.9, "1": 0.1})
```

**Fix**:
```python
# After loading config values, add validation method
self.min_attendees = self._config.get("min_attendees", 2)
self.max_attendees = self._config.get("max_attendees", 8)
self.primary_id_weights = self._config.get("primary_id_weights", {"2": 0.9, "1": 0.1})

# Validate configuration values
self._validate_config()

def _validate_config(self) -> None:
    """Validate configuration values are logically consistent.

    Raises:
        ValueError: If configuration values are invalid
    """
    # Validate attendee ranges
    if self.min_attendees < 1:
        raise ValueError(f"min_attendees must be >= 1, got {self.min_attendees}")

    if self.max_attendees < self.min_attendees:
        raise ValueError(
            f"max_attendees ({self.max_attendees}) must be >= "
            f"min_attendees ({self.min_attendees})"
        )

    # Validate ID weights
    if self.primary_id_weights:
        total_weight = sum(self.primary_id_weights.values())
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point variance
            warnings.warn(
                f"primary_id_weights sum to {total_weight:.3f}, expected ~1.0. "
                f"Weights will be normalized."
            )
```

**Why**: Catches configuration errors early with clear error messages.

---

## PHASE 2: HIGH PRIORITY - ERROR HANDLING & TYPE SAFETY

### 2.1 Replace Bare Exception Handlers

**Severity**: HIGH
**Files**:
- `src/saisonxform/cli.py:37,393,510`
- `src/saisonxform/io.py:54,110`
- `web_app.py:320`

**Issue**: Bare `except Exception` catches all exceptions including `SystemExit`, `KeyboardInterrupt`.

**Pattern to Fix**:
```python
# BEFORE (cli.py:37)
try:
    result = subprocess.run(...)
    return result.returncode == 0 and result.stdout.strip() == "true"
except Exception:
    return False

# AFTER
try:
    result = subprocess.run(...)
    return result.returncode == 0 and result.stdout.strip() == "true"
except (OSError, subprocess.SubprocessError) as e:
    # Log specific error for debugging
    if verbose:
        print(f"Git check failed: {e}", file=sys.stderr)
    return False
```

**All Locations to Update**:

1. **cli.py:37** - Catch `(OSError, subprocess.SubprocessError)`
2. **cli.py:393** - Catch `(ValueError, KeyError, pd.errors.ParserError)` for CSV processing
3. **cli.py:510** - Catch `(FileNotFoundError, ValueError, PermissionError)`
4. **io.py:54** - Catch `(OSError, chardet.UniversalDetectorError)` if chardet has specific errors
5. **io.py:110** - Catch `(OSError, UnicodeError)`
6. **web_app.py:320** - Catch `(FileNotFoundError, PermissionError)` or remove silent pass

**Why**: More specific exception handling improves debugging and prevents hiding critical errors.

---

### 2.2 Modernize Type Hints (Python 3.10+ Syntax)

**Severity**: MEDIUM
**Files**: `src/saisonxform/selectors.py:74`, `src/saisonxform/config.py:104`

**Issue**: Using old-style `Union[X, Y]` when Python 3.10+ supports `X | Y`.

**Current Code** (`selectors.py:74`):
```python
from typing import Union

def sample_attendee_ids(
    count: int,
    available_ids: list[str],
    id_2_weight: float = 0.9,
    id_1_weight: float = 0.1,
    return_dict: bool = False,
) -> Union[list[str], dict[str, str]]:
```

**Fix**:
```python
# Remove Union import, use | syntax
def sample_attendee_ids(
    count: int,
    available_ids: list[str],
    id_2_weight: float = 0.9,
    id_1_weight: float = 0.1,
    return_dict: bool = False,
) -> list[str] | dict[str, str]:
```

**Similar Fix** (`config.py:104`):
```python
# BEFORE
def _load_amount_based_config(self) -> dict[str, Any] | None:

# Keep this - already correct!
```

**Why**: Cleaner syntax, project targets Python 3.10+.

---

### 2.3 Add Missing Type Hints

**Severity**: MEDIUM
**Files**: `src/saisonxform/reporting.py`, `web_app.py:69,183,272`

**Locations to Add Type Hints**:

1. **reporting.py:9-54** - `get_unique_attendees()` function
2. **web_app.py:69** - `process_file()` return type should be `dict[str, Any]`
3. **web_app.py:183** - `render_editor()` should specify return type `None`
4. **web_app.py:272** - `generate_report()` already has return type `str` ✓

**Example Fix** (`web_app.py:69`):
```python
# BEFORE
def process_file(filename: str, file_bytes: bytes) -> dict:

# AFTER
from typing import Any

def process_file(filename: str, file_bytes: bytes) -> dict[str, Any]:
    """Process a single uploaded file.

    Args:
        filename: Name of the file
        file_bytes: File content as bytes

    Returns:
        Dictionary with keys: 'df', 'encoding', 'pre_header', 'unique_attendees'
    """
```

---

### 2.4 Fix Type Coercion Inconsistencies

**Severity**: MEDIUM
**Files**: `web_app.py:287`

**Issue**: Using nullable `Int64` dtype creates type confusion in templates.

**Current Code**:
```python
report_df["人数"] = pd.to_numeric(report_df["人数"], errors="coerce").astype("Int64")
```

**Fix**:
```python
# Convert to regular int, filling NaN with 0 or empty string depending on use case
report_df["人数"] = (
    pd.to_numeric(report_df["人数"], errors="coerce")
    .fillna(0)  # Or .fillna("") if template expects string
    .astype(int)
)
```

**Why**: Consistent integer type throughout pipeline prevents template rendering issues.

---

### 2.5 Improve Error Messages with Context

**Severity**: MEDIUM
**Files**: `src/saisonxform/cli.py:394`, `web_app.py`, `src/saisonxform/reporting.py:48`

**Issue**: Generic error messages lack context about which file/step failed.

**Pattern to Fix**:
```python
# BEFORE (cli.py:394)
except Exception as e:
    typer.echo(f"  ✗ ERROR: {e}")
    error_count += 1

# AFTER
except Exception as e:
    typer.echo(f"  ✗ ERROR processing {csv_file.name}: {e}")
    typer.echo(f"     File path: {csv_file}")
    typer.echo(f"     Step: CSV reading/processing")
    if verbose:
        import traceback
        typer.echo(f"     Traceback: {traceback.format_exc()}")
    error_count += 1
```

---

## PHASE 3: MEDIUM PRIORITY - CODE QUALITY & TESTING

### 3.1 Extract Magic Numbers to Module Constants

**Severity**: MEDIUM
**Files**: `src/saisonxform/io.py:21,86`, `src/saisonxform/cli.py:198`

**Current Code**:
```python
# io.py:21
CHARDET_CONFIDENCE_THRESHOLD = 0.6  # Already defined ✓

# io.py:86
if idx >= 20:  # Magic number - should be constant

# cli.py:198
months_to_process = get_latest_months(config.input_dir, n=2)  # Magic number
```

**Fix**:
```python
# Add to top of io.py
MAX_HEADER_SCAN_ROWS = 20  # Maximum rows to scan for header

# Add to top of cli.py or config
DEFAULT_LATEST_MONTHS = 2  # Default number of months to process

# Usage
if idx >= MAX_HEADER_SCAN_ROWS:
    break

months_to_process = get_latest_months(config.input_dir, n=DEFAULT_LATEST_MONTHS)
```

---

### 3.2 Extract Lambda to Named Function

**Severity**: LOW
**Files**: `src/saisonxform/reporting.py:51`, `src/saisonxform/selectors.py:135`

**Current Code** (`reporting.py:51`):
```python
result["_sort_key"] = result["ID"].apply(lambda x: int(x) if x.isdigit() else float("inf"))
```

**Fix**:
```python
def _numeric_sort_key(id_value: str) -> int | float:
    """Convert ID to numeric sort key, placing non-numeric IDs at end.

    Args:
        id_value: ID string value

    Returns:
        Integer value for numeric IDs, infinity for non-numeric
    """
    return int(id_value) if id_value.isdigit() else float("inf")

# Usage
result["_sort_key"] = result["ID"].apply(_numeric_sort_key)
```

**Why**: Easier to test, debug, and reuse.

---

### 3.3 Create Web App Unit Tests

**Severity**: HIGH
**Files**: None (missing `tests/test_web_app.py`)

**Issue**: No unit tests for `web_app.py` (394 lines of untested code).

**Create**: `tests/test_web_app.py`

**Suggested Test Cases**:
```python
"""Unit tests for web_app.py."""
import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from web_app import (
    process_file,
    generate_report,
    load_attendee_reference,
)


class TestLoadAttendeeReference:
    """Test attendee reference loading."""

    def test_load_existing_file(self, tmp_path):
        """Should load valid CSV file."""
        ref_file = tmp_path / "NameList.csv"
        ref_file.write_text("ID,Name,Title,Company\n1,Test,Manager,Corp\n")

        result = load_attendee_reference(ref_file)

        assert result is not None
        assert len(result) == 1
        assert result.iloc[0]["Name"] == "Test"

    def test_missing_file(self, tmp_path):
        """Should return None for missing file."""
        result = load_attendee_reference(tmp_path / "missing.csv")
        assert result is None


class TestProcessFile:
    """Test file processing logic."""

    @patch('streamlit.session_state')
    def test_process_valid_csv(self, mock_session_state, sample_csv_bytes, sample_attendee_ref):
        """Should process valid CSV with attendee assignment."""
        mock_session_state.attendee_ref = sample_attendee_ref
        mock_session_state.config = Mock(
            min_attendees=2,
            max_attendees=8,
            amount_based_attendees=None,
            primary_id_weights={"2": 0.9, "1": 0.1}
        )

        result = process_file("test.csv", sample_csv_bytes)

        assert "df" in result
        assert "encoding" in result
        assert "pre_header" in result
        assert "unique_attendees" in result
        assert isinstance(result["df"], pd.DataFrame)

    @patch('streamlit.session_state')
    def test_process_empty_file(self, mock_session_state):
        """Should raise ValueError for empty file."""
        mock_session_state.attendee_ref = pd.DataFrame()

        with pytest.raises(ValueError, match="File is empty"):
            process_file("empty.csv", b"")


class TestGenerateReport:
    """Test HTML report generation."""

    @patch('streamlit.session_state')
    def test_generate_html_report(self, mock_session_state, sample_processed_data):
        """Should generate valid HTML report."""
        mock_session_state.attendee_ref = pd.DataFrame({
            "ID": ["1", "2"],
            "Name": ["Test1", "Test2"]
        })

        html = generate_report(sample_processed_data)

        assert isinstance(html, str)
        assert "<!DOCTYPE html>" in html or "<html" in html
        assert len(html) > 100  # Non-empty HTML


# Fixtures
@pytest.fixture
def sample_csv_bytes():
    """Sample CSV file as bytes."""
    csv_content = """利用日,ご利用店名及び商品名,利用金額,科目＆No.
2025-01-10,Restaurant,15000,会議費
"""
    return csv_content.encode('utf-8')


@pytest.fixture
def sample_attendee_ref():
    """Sample attendee reference DataFrame."""
    return pd.DataFrame({
        "ID": ["1", "2", "3"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Title": ["Manager", "Lead", "Developer"],
        "Company": ["Corp A", "Corp B", "Corp C"]
    })


@pytest.fixture
def sample_processed_data():
    """Sample processed file data."""
    return {
        "df": pd.DataFrame({
            "利用日": ["2025-01-10"],
            "ご利用店名及び商品名": ["Restaurant"],
            "利用金額": [15000],
            "科目＆No.": ["会議費"],
            "人数": [3],
            "ID1": ["1"],
            "ID2": ["2"],
            "ID3": ["3"],
            "ID4": [""],
            "ID5": [""],
            "ID6": [""],
            "ID7": [""],
            "ID8": [""],
            "備考": [""]
        }),
        "encoding": "utf-8",
        "pre_header": [],
        "unique_attendees": []
    }
```

**Test Coverage Target**: Add ~200-300 lines of tests to achieve 90%+ coverage of web_app.py.

---

### 3.4 Add Test Determinism (Seed Randomness)

**Severity**: MEDIUM
**Files**: `tests/test_selectors.py:63-65`

**Issue**: Tests use randomness without seeding, causing non-deterministic failures.

**Current Code**:
```python
for _ in range(20):  # Non-deterministic tests
    count = estimate_attendee_count(...)
    assert 2 <= count <= 8
```

**Fix**:
```python
import random

def test_estimate_attendee_count_random_distribution():
    """Test that random distribution stays within bounds."""
    random.seed(42)  # Make test deterministic

    results = []
    for _ in range(20):
        count = estimate_attendee_count(5000, min_attendees=2, max_attendees=8)
        results.append(count)
        assert 2 <= count <= 8

    # Additional assertion: verify distribution is reasonably uniform
    assert len(set(results)) > 1, "Should generate different values"
```

---

### 3.5 Create Shared Test Fixtures in conftest.py

**Severity**: LOW
**Files**: Create `tests/conftest.py`

**Issue**: Duplicate fixture definitions across test files.

**Create**:
```python
"""Shared pytest fixtures for Saison Transform tests."""
import pandas as pd
import pytest
from pathlib import Path


@pytest.fixture
def sample_attendee_ref():
    """Standard attendee reference DataFrame for testing."""
    return pd.DataFrame({
        "ID": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"],
        "Title": ["Manager", "Lead", "Developer", "Analyst", "Designer", "QA", "PM", "Director"],
        "Company": ["Corp A", "Corp B", "Corp C", "Corp D", "Corp E", "Corp F", "Corp G", "Corp H"]
    })


@pytest.fixture
def sample_config_dict():
    """Standard configuration dictionary for testing."""
    return {
        "min_attendees": 2,
        "max_attendees": 8,
        "primary_id_weights": {"2": 0.9, "1": 0.1},
        "input_dir": "data/input",
        "reference_dir": "data/reference",
        "output_dir": "data/output",
        "archive_dir": "data/archive",
    }


@pytest.fixture
def sample_transaction_df():
    """Sample transaction DataFrame for testing."""
    return pd.DataFrame({
        "利用日": ["2025-01-10", "2025-01-15"],
        "ご利用店名及び商品名": ["Restaurant A", "Cafe B"],
        "利用金額": [15000, 8000],
        "科目＆No.": ["会議費", "接待費"]
    })
```

---

## PHASE 4: DEPENDENCY & SECURITY UPDATES

### 4.1 Unpin Dependency Versions

**Severity**: MEDIUM
**Files**: `pyproject.toml:15-16`

**Current Code**:
```toml
typer = "0.9.0"  # Pinned from Jan 2024
click = "8.1.3"  # Pinned from Jan 2024
```

**Fix**:
```toml
typer = "^0.9.0"  # Allow patch/minor updates
click = "^8.1.3"  # Allow patch/minor updates
```

**Then Run**:
```bash
poetry update typer click
poetry lock
```

**Why**: Get security patches and bug fixes while maintaining compatibility.

---

### 4.2 Add CSV Injection Prevention

**Severity**: MEDIUM
**Files**: `src/saisonxform/io.py:199-242`

**Issue**: CSV files may contain formula injection (e.g., `=1+1` in cells).

**Add Function**:
```python
def _escape_csv_formulas(value: str) -> str:
    """Escape potential CSV formula injection.

    Args:
        value: Cell value to escape

    Returns:
        Escaped value safe for CSV export
    """
    if isinstance(value, str) and value.startswith(('=', '+', '-', '@', '\t', '\r')):
        return "'" + value  # Prefix with single quote to escape
    return value


def write_csv_utf8_bom(
    df: pd.DataFrame,
    file_path: Path,
    handle_duplicates: bool = False,
    pre_header_rows: Optional[list[str]] = None,
) -> Path:
    """Write DataFrame to CSV with UTF-8 BOM encoding and formula escaping."""
    output_path = Path(file_path)

    # ... existing duplicate handling ...

    # Escape formulas in all string columns
    df_escaped = df.copy()
    for col in df_escaped.columns:
        if df_escaped[col].dtype == object:  # String columns
            df_escaped[col] = df_escaped[col].apply(
                lambda x: _escape_csv_formulas(x) if isinstance(x, str) else x
            )

    # Write with UTF-8 BOM (use df_escaped instead of df)
    # ... rest of existing code ...
```

---

### 4.3 Add Environment Variable Documentation

**Severity**: LOW
**Files**: `README.md` or create `docs/ENVIRONMENT_VARIABLES.md`

**Create Documentation**:
```markdown
# Environment Variables

Saison Transform supports the following environment variables for configuration:

## Directory Paths

- `INPUT_DIR`: Override input directory path (default: `data/input`)
- `REFERENCE_DIR`: Override reference directory path (default: `data/reference`)
- `OUTPUT_DIR`: Override output directory path (default: `data/output`)
- `ARCHIVE_DIR`: Override archive directory path (default: `data/archive`)

## Feature Flags

- `SAISONXFORM_SKIP_GIT_VALIDATION`: Skip git repository validation (values: `1`, `true`, `yes`)
  - Default: `false`
  - Use case: Testing environments, CI/CD pipelines

## Precedence

Environment variables have highest precedence, overriding:
1. Explicit `--config` file
2. `data/reference/config.toml`
3. `config.toml` (project root)
4. `pyproject.toml` defaults

## Examples

```bash
# Override input directory
export INPUT_DIR=/path/to/custom/input
sf --verbose

# Skip git validation in CI
export SAISONXFORM_SKIP_GIT_VALIDATION=true
sf --month 202501
```
```

---

## PHASE 5: OPTIMIZATION & PERFORMANCE

### 5.1 Optimize DataFrame Copy Operations

**Severity**: LOW
**Files**: `web_app.py:190,249,253,278`

**Issue**: Multiple unnecessary `.copy()` calls on large DataFrames.

**Current Code**:
```python
file_data = st.session_state.processed_files[filename].copy()  # Line 190
df = file_data["df"].copy()  # Line 190
# ... later ...
st.session_state.processed_files[filename]["df"] = df.copy()  # Line 253
```

**Fix Strategy**:
1. Only copy when mutation is needed
2. Use views where possible
3. Clear processed files after download

```python
# In render_editor function
file_data = st.session_state.processed_files[filename]  # No copy
df = file_data["df"]  # Work with reference

# Only copy when actually editing
if not edited_df.equals(display_df):
    # Only now do we need a copy
    st.session_state.processed_files[filename]["df"] = edited_df.copy()
```

**Add Cleanup** (in download step):
```python
# After successful download, clear processed data to free memory
if st.button("Clear Processed Files"):
    st.session_state.processed_files.clear()
    st.success("Memory cleared")
    st.rerun()
```

---

### 5.2 Optimize Encoding Detection for Large Files

**Severity**: LOW
**Files**: `src/saisonxform/io.py:40-41`

**Issue**: Reads entire file into memory for encoding detection.

**Current Code**:
```python
with open(file_path, "rb") as f:
    raw_data = f.read()  # Entire file!
```

**Fix**:
```python
# Read only first 10KB for detection (sufficient for encoding)
MAX_DETECTION_BYTES = 10240  # 10KB

with open(file_path, "rb") as f:
    raw_data = f.read(MAX_DETECTION_BYTES)
```

**Why**: Faster for large files, still accurate for encoding detection.

---

### 5.3 Optimize Pandas DataFrame Operations

**Severity**: LOW
**Files**: `src/saisonxform/reporting.py:80-87`

**Current Code**:
```python
for col in transactions_copy.columns:
    if isinstance(transactions_copy[col].dtype, pd.Int64Dtype):
        transactions_copy[col] = transactions_copy[col].astype(float).astype(object)
```

**Fix**:
```python
# More efficient: use select_dtypes and vectorized operations
int64_cols = transactions_copy.select_dtypes(include=['Int64']).columns
for col in int64_cols:
    transactions_copy[col] = transactions_copy[col].astype(float).astype(object)
```

**Better Fix**:
```python
# Even better: avoid intermediate float conversion
int64_cols = transactions_copy.select_dtypes(include=['Int64']).columns
transactions_copy[int64_cols] = transactions_copy[int64_cols].astype(object)
```

---

## PHASE 6: DOCUMENTATION & DEVELOPER EXPERIENCE

### 6.1 Add --config-info Command

**Severity**: MEDIUM
**Files**: `src/saisonxform/cli.py` (new command)

**Purpose**: Help users debug configuration issues.

**Implementation**:
```python
@app.command(name="config-info")
def show_config_info(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.toml file",
    ),
) -> None:
    """Display active configuration and sources.

    Shows which configuration files are being used and the precedence chain.
    """
    typer.echo("\n📋 Configuration Information\n")

    config = Config(config_file=config_file)

    # Show config file sources
    typer.echo("Configuration Sources (in precedence order):")
    typer.echo("  1. Environment variables:")
    for env_var in ["INPUT_DIR", "REFERENCE_DIR", "OUTPUT_DIR", "ARCHIVE_DIR"]:
        value = os.getenv(env_var)
        if value:
            typer.echo(f"     • {env_var}={value}")
        else:
            typer.echo(f"     • {env_var}=(not set)")

    typer.echo("\n  2. Config file:")
    if config.config_file:
        typer.echo(f"     • Explicit: {config.config_file}")
    else:
        ref_config = Path("data/reference/config.toml")
        root_config = Path("config.toml")
        if ref_config.exists():
            typer.echo(f"     • Using: {ref_config}")
        elif root_config.exists():
            typer.echo(f"     • Using: {root_config}")
        else:
            typer.echo("     • None found, using defaults")

    typer.echo("\n  3. Project defaults: pyproject.toml")

    # Show effective configuration
    typer.echo("\n📁 Effective Directory Configuration:")
    typer.echo(f"  • Input:     {config.input_dir}")
    typer.echo(f"  • Reference: {config.reference_dir}")
    typer.echo(f"  • Output:    {config.output_dir}")
    typer.echo(f"  • Archive:   {config.archive_dir}")

    typer.echo("\n⚙️  Processing Configuration:")
    typer.echo(f"  • Min attendees: {config.min_attendees}")
    typer.echo(f"  • Max attendees: {config.max_attendees}")
    typer.echo(f"  • Primary ID weights: {config.primary_id_weights}")

    if config.amount_based_attendees:
        typer.echo(f"  • Amount-based estimation: Enabled")
        typer.echo(f"    - Cost per person: ¥{config.amount_based_attendees['cost_per_person']}")
    else:
        typer.echo(f"  • Amount-based estimation: Disabled (random)")

    typer.echo()
```

**Usage**:
```bash
sf config-info
sf config-info --config custom_config.toml
```

---

### 6.2 Add Architecture Documentation

**Severity**: LOW
**Files**: Create `docs/ARCHITECTURE.md`

**Content** (excerpt):
```markdown
# Saison Transform Architecture

## Overview

Saison Transform follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         User Interfaces                 │
│  ┌──────────┐        ┌──────────────┐  │
│  │ CLI (sf) │        │ Streamlit UI │  │
│  └────┬─────┘        └──────┬───────┘  │
│       │                     │           │
└───────┼─────────────────────┼───────────┘
        │                     │
        ▼                     ▼
┌─────────────────────────────────────────┐
│         Core Modules                    │
│  ┌──────────┬──────────┬──────────┐    │
│  │ io.py    │config.py │selectors │    │
│  │ (I/O)    │ (Config) │ (Logic)  │    │
│  └──────────┴──────────┴──────────┘    │
│  ┌──────────┬──────────┐               │
│  │reporting │month_    │               │
│  │ (HTML)   │ utils    │               │
│  └──────────┴──────────┘               │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│         Data Layer                      │
│  ┌──────────┬──────────┬──────────┐    │
│  │ Input/   │Reference │ Archive/ │    │
│  │ (CSVs)   │(NameList)│ (History)│    │
│  └──────────┴──────────┴──────────┘    │
└─────────────────────────────────────────┘
```

## Module Responsibilities

### io.py
- CSV reading with encoding detection
- UTF-8 BOM writing
- Header detection
- Pre-header row extraction

### config.py
- Multi-source configuration loading
- Path resolution
- Configuration validation
- Environment variable support

### selectors.py
- Attendee count estimation
- ID sampling with weights
- Transaction filtering

### reporting.py
- HTML report generation (Jinja2)
- Unique attendee extraction
- Data formatting for display

### month_utils.py
- Archive management
- Month extraction
- Retry markers
- File operations

## Data Flow

1. **Input**: CSV files (various encodings)
2. **Detection**: Auto-detect encoding, find header
3. **Processing**: Estimate attendees, assign IDs
4. **Output**: CSV (UTF-8 BOM) + HTML report
5. **Archive**: Move input to Archive/YYYYMM/

## Configuration Precedence

1. Environment variables (highest)
2. Explicit --config file
3. data/reference/config.toml
4. config.toml (project root)
5. pyproject.toml defaults (lowest)
```

---

### 6.3 Improve Docstring Coverage

**Severity**: LOW
**Files**: All modules

**Add Missing Docstrings** for:
1. All public functions (those without leading `_`)
2. All classes
3. Complex private functions

**Standard Format** (Google style):
```python
def function_name(arg1: type1, arg2: type2) -> return_type:
    """One-line summary.

    Longer description if needed, explaining the purpose,
    algorithm, or important details.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
        FileNotFoundError: When file not found

    Examples:
        >>> function_name(value1, value2)
        expected_result
    """
```

---

## IMPLEMENTATION CHECKLIST

Use this checklist to track progress:

### Phase 1: Critical Fixes (Est: 2-3 hours)
- [ ] 1.1 Replace assertions with type checks (cli.py:337, web_app.py:159)
- [ ] 1.2 Fix temp file security (web_app.py:102-108)
- [ ] 1.3 Add path traversal validation (config.py:168-180)
- [ ] 1.4 Fix config default inconsistencies (config.py properties)
- [ ] 1.5 Add configuration validation (config.py:54-56)

### Phase 2: Error Handling & Types (Est: 3-4 hours)
- [ ] 2.1 Replace 6 bare exception handlers
- [ ] 2.2 Modernize type hints to X | Y syntax
- [ ] 2.3 Add missing type hints (4 locations)
- [ ] 2.4 Fix Int64 dtype coercion (web_app.py:287)
- [ ] 2.5 Improve 3 error messages with context

### Phase 3: Code Quality & Testing (Est: 4-6 hours)
- [ ] 3.1 Extract 3 magic numbers to constants
- [ ] 3.2 Extract 2 lambdas to named functions
- [ ] 3.3 Create web_app unit tests (200-300 lines)
- [ ] 3.4 Add random.seed() to 3 test functions
- [ ] 3.5 Create tests/conftest.py with shared fixtures

### Phase 4: Dependencies & Security (Est: 1-2 hours)
- [ ] 4.1 Unpin typer/click versions
- [ ] 4.2 Add CSV formula injection escaping
- [ ] 4.3 Document environment variables

### Phase 5: Performance (Est: 1-2 hours)
- [ ] 5.1 Optimize DataFrame copy operations (4 locations)
- [ ] 5.2 Limit encoding detection to 10KB
- [ ] 5.3 Optimize Int64 dtype conversions

### Phase 6: Documentation (Est: 2-3 hours)
- [ ] 6.1 Add `sf config-info` command
- [ ] 6.2 Create ARCHITECTURE.md
- [ ] 6.3 Add missing docstrings (estimate ~20 functions)

### Final Steps
- [ ] Run full test suite: `poetry run pytest --cov`
- [ ] Run type checking: `poetry run mypy src`
- [ ] Run linting: `poetry run ruff check src tests`
- [ ] Run security scan: `poetry run bandit -r src`
- [ ] Run formatting: `poetry run black src tests`
- [ ] Update CHANGELOG.md with all changes
- [ ] Bump version to 0.3.0 in pyproject.toml
- [ ] Commit changes: `git commit -m "fix: comprehensive codebase improvements (v0.3.0)"`
- [ ] Create pull request

---

## TESTING STRATEGY

After implementing each phase:

1. **Unit Tests**: Run specific test module
   ```bash
   poetry run pytest tests/test_[module].py -v
   ```

2. **Coverage Check**: Verify coverage stays above 90%
   ```bash
   poetry run pytest --cov=saisonxform --cov-report=term-missing
   ```

3. **Integration Test**: Run demo end-to-end
   ```bash
   poetry run sf demo --output /tmp/demo-test
   cd /tmp/demo-test
   poetry run sf --verbose
   ```

4. **Security Scan**: Check for new vulnerabilities
   ```bash
   poetry run bandit -r src
   ```

---

## PRIORITY MATRIX

| Fix | Impact | Effort | Priority | Phase |
|-----|--------|--------|----------|-------|
| Assertions → Exceptions | Critical | Low | **P0** | 1.1 |
| Temp file security | Critical | Low | **P0** | 1.2 |
| Path traversal | Critical | Medium | **P0** | 1.3 |
| Config validation | High | Medium | **P1** | 1.5 |
| Config defaults | High | Low | **P1** | 1.4 |
| Web app tests | High | High | **P1** | 3.3 |
| Bare exceptions | High | Medium | **P1** | 2.1 |
| Type hints | Medium | Low | **P2** | 2.2, 2.3 |
| Magic numbers | Low | Low | **P3** | 3.1 |
| Documentation | Low | Medium | **P3** | 6.x |

---

## SUCCESS CRITERIA

After completing all phases:

✅ **Security**: All CRITICAL vulnerabilities fixed
✅ **Reliability**: No assertions in production code
✅ **Type Safety**: mypy passes with no errors
✅ **Test Coverage**: ≥90% (including web_app.py)
✅ **Code Quality**: ruff and black pass
✅ **Documentation**: All public APIs documented
✅ **Performance**: No unnecessary DataFrame copies
✅ **Developer Experience**: `sf config-info` command available

---

## NOTES FOR IMPLEMENTER

1. **Work Incrementally**: Complete each phase before moving to the next
2. **Test After Each Fix**: Don't accumulate untested changes
3. **Commit Frequently**: One logical change per commit
4. **Update Tests First**: For bugs, write failing test → fix → verify
5. **Check Dependencies**: Run `poetry lock` after dependency changes
6. **Verify No Regressions**: Full test suite must pass after each phase

---

**Document Version**: 1.0
**Last Updated**: 2026-01-23
**Estimated Total Effort**: 13-20 hours
**Recommended Timeline**: 3-5 working days
