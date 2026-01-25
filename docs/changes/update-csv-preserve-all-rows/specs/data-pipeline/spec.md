# data-pipeline Delta Specification

## MODIFIED Requirements

### Requirement: CSV Parsing Rules
The pipeline MUST statically detect header rows, dynamically locate transaction rows, preserve all pre-header rows, and tolerate encoding differences or missing columns per the spec.

#### Scenario: Header detection algorithm
- **WHEN** a CSV has headers on any of the first 10 rows
- **THEN** the parser scans line-by-line until it finds a row containing all required column titles (`利用日`, `ご利用店名及び商品名`, `利用金額`, `備考`), treats that row as the header, treats the following row as the first transaction, and preserves all rows before the header row as pre-header metadata.

#### Scenario: Pre-header row preservation
- **WHEN** a CSV has metadata or summary rows before the header row
- **THEN** the parser preserves those rows exactly as-is (without modification or attendee columns) and includes them at the beginning of the output CSV file.

#### Scenario: No pre-header rows
- **WHEN** a CSV has the header row on the first line (no pre-header rows)
- **THEN** the parser behaves as before, processing only the header and data rows without any pre-header content.

#### Scenario: Encoding detection and fallback
- **WHEN** chardet returns a low confidence (<0.6) or fails to detect encoding
- **THEN** the pipeline attempts `utf-8-sig`, `utf-8`, and `cp932` in order, logging the encoding actually used; mixed encodings within one file trigger a warning and result in UTF-8 output.

#### Scenario: Graceful degradation
- **WHEN** required columns (e.g., `備考`) are missing or a file is empty
- **THEN** the pipeline logs warnings, attempts to continue processing remaining files, and emits minimal placeholder reports rather than crashing.

## MODIFIED Requirements

### Requirement: Output Schema Consistency
Processed CSVs MUST preserve all pre-header rows (if any), add separate columns `出席者`, `ID1` through `ID8` to data rows only, leaving blank strings when fewer IDs exist, and HTML reports MUST display only the transaction data (not pre-header metadata).

#### Scenario: Pre-header preservation in output
- **WHEN** input CSV contains pre-header rows before the data header
- **THEN** output CSV includes those pre-header rows at the beginning, unchanged, followed by the header row with added attendee columns, followed by data rows with attendee data populated.

#### Scenario: Sparse attendees
- **WHEN** only three attendees are selected
- **THEN** `ID4`–`ID8` are emitted as empty fields in the CSV, and the HTML shows only populated IDs without introducing placeholder text.
