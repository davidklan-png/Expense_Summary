# Change: Preserve All CSV Rows Including Pre-Header Data

## Why
Currently, CSV files may contain metadata or header rows before the actual data header. The current implementation skips all rows before the detected header row, discarding potentially important metadata. Users need to preserve ALL data from the original CSV file, including pre-header rows, in the output file.

## What Changes
- Update CSV parsing logic to preserve all rows before the header row as-is
- Output CSV will contain: pre-header rows (if any) + header row + all data rows
- Pre-header rows will be written as-is without modification (no attendee columns added to these rows)
- Only data rows (after header) will have attendee columns added

## Impact
- Affected specs: data-pipeline
- Affected code: `src/saisonxform/io.py` (CSV reading/writing functions)
- Affected tests: `tests/test_io.py` (new test cases for pre-header preservation)
- **BREAKING**: None - this is backward compatible (files without pre-header rows work as before)
