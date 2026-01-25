# Data Pipeline Specification Delta

This delta spec documents corrections to the implementation that deviated from the approved specification.

## MODIFIED Requirements

### Requirement: CLI Architecture
The CLI MUST be implemented with Typer to provide a `saisonxform` console script plus `sf` alias, supporting subcommands for `run` (default) and `validate-config`.

#### Scenario: Console script exposure
- **WHEN** Poetry installs the project
- **THEN** `pyproject.toml` defines two `console_scripts` entries—`saisonxform` and `sf`—both invoking the same Typer app that mirrors `python -m saisonxform.cli` behavior.

#### Scenario: Module parity
- **WHEN** a user runs `python -m saisonxform.cli run`
- **THEN** it executes the same code path as the console scripts, ensuring documentation references remain accurate.

#### Scenario: Subcommand clarity
- **WHEN** `saisonxform --help` is executed
- **THEN** it lists at least `run` (process files) and `validate-config` (checks config + directories) with consistent options.

#### Scenario: Run command options
- **WHEN** `saisonxform run --help` is executed
- **THEN** it shows options for `--month` (repeatable), `--force`, `--input`, `--reference`, `--output`, `--archive`, and `--config`.

#### Scenario: Validate-config with dry-run
- **WHEN** `saisonxform validate-config --dry-run` is executed
- **THEN** it validates configuration and directory existence without creating directories or processing files, and exits with status 0 if valid or non-zero with error messages if invalid.

#### Scenario: Backward compatibility
- **WHEN** a user runs bare `saisonxform` or `saisonxform process`
- **THEN** the CLI emits a deprecation warning suggesting `saisonxform run` and executes the run command for backward compatibility during migration period.

### Requirement: CLI Invocation and Month Selection
The project MUST expose a console script named `saisonxform` (alias `sf`) that accepts configuration overrides and month filters for processing.

#### Scenario: Explicit month arguments
- **GIVEN** a user runs `saisonxform run --config config.toml --month 202510 --month 202511`
- **THEN** only data for the specified year-month pairs is processed, and Input/Reference/Output/Archive paths come from the provided config (unless overridden by `--input/--reference/--output/--archive`).

#### Scenario: Default month window
- **GIVEN** no `--month` arguments are supplied
- **WHEN** the command executes
- **THEN** it automatically selects the latest two months relative to filenames in Input/ (by parsing YYYYMM prefixes) and processes only those statements.

#### Scenario: Path overrides
- **WHEN** a user passes `--input`, `--reference`, `--output`, or `--archive` on the CLI
- **THEN** those values temporarily override the corresponding entries in `config.toml` for that invocation without persisting changes, and the precedence order (CLI > env vars > config > pyproject) is logged once per run.

#### Scenario: Precedence logging
- **WHEN** `saisonxform run` starts
- **THEN** it logs the effective configuration source for each path (e.g., "input_dir: /data/input (from CLI --input)"), showing the precedence order that was applied.

### Requirement: Month Selection
Default month processing MUST operate on filename prefixes shaped as `YYYYMM*`, with fallback to explicit CLI months.

#### Scenario: Filename-based detection
- **WHEN** no `--month` flag is supplied
- **THEN** the CLI enumerates files in `Input/`, identifies those whose names start with `YYYYMM` (6 digits), sorts them descending, and processes only the latest two distinct months.

#### Scenario: Mixed naming patterns
- **WHEN** files do not match the `YYYYMM` pattern
- **THEN** the CLI logs a warning and skips them unless explicit `--month` flags were provided that match the ambiguous files.

#### Scenario: No matching files
- **WHEN** Input/ contains no files matching the selected month(s)
- **THEN** the CLI exits with status 0 and logs "No files found for month(s): 202510, 202511" without error.

### Requirement: Post-Processing Archival
After successfully processing individual CSVs, each raw file MUST be moved from `Input/` to the configured `Archive/` directory to prevent reprocessing; the `Archive/` directory is auto-created if it does not exist.

#### Scenario: Per-file archival granularity
- **WHEN** a file (e.g., `202510_A.csv`) is successfully processed
- **THEN** that specific file is immediately moved to `Archive/202510/202510_A.csv`, creating both `Archive/` and the month subdirectory if needed, independent of whether other files in the same month succeed or fail.

#### Scenario: Partial month processing
- **WHEN** processing month `202510` with 5 input files, where 4 succeed and 1 fails
- **THEN** the 4 successful files are archived to `Archive/202510/`, the 1 failed file remains in `Input/`, and a retry marker file `Archive/.retry_202510.json` is created containing `{"month": "202510", "failed_files": ["202510_E.csv"], "timestamp": "2025-11-07T10:30:00Z", "errors": [{"file": "202510_E.csv", "error": "Missing required column: 備考"}]}`.

#### Scenario: Already-archived month detection
- **WHEN** a user explicitly requests `--month 202510` and `Archive/202510/` exists without a retry marker
- **THEN** the CLI exits immediately with error status and message "Month 202510 already processed. Use --force to reprocess." without scanning `Input/`.

#### Scenario: Force reprocessing
- **WHEN** a user passes `--month 202510 --force` and archived files exist
- **THEN** the CLI processes any matching files found in `Input/`, archives them per normal flow to `Archive/202510/`, and logs a warning that this may create duplicate outputs.

#### Scenario: Archive directory auto-creation
- **WHEN** the first archival operation runs and `Archive/` does not exist
- **THEN** the CLI creates `Archive/` at the configured path (relative or absolute), logs the creation, and proceeds with archival.

#### Scenario: Archive failure handling
- **WHEN** archival fails for a file (e.g., permissions, disk full, cross-filesystem move error)
- **THEN** the CLI emits an error, creates/updates the retry marker file `Archive/.retry_YYYYMM.json` with failure details, leaves the unarchived file in `Input/`, and continues processing remaining files before exiting with non-zero status.

### Requirement: Retry Marker Format
Retry marker files MUST be JSON documents stored as `Archive/.retry_YYYYMM.json` containing structured failure information for operator intervention.

#### Scenario: Marker file structure
- **WHEN** a retry marker is created for month `202510`
- **THEN** the file `Archive/.retry_202510.json` contains at minimum: `{"month": "202510", "failed_files": ["filename1.csv", ...], "timestamp": "ISO8601", "errors": [{"file": "filename1.csv", "error": "error message"}]}`.

#### Scenario: Marker cleanup on success
- **WHEN** all previously failed files in a month are successfully processed and archived
- **THEN** the corresponding `.retry_YYYYMM.json` file is deleted, signaling full completion.

#### Scenario: Marker update on new failures
- **WHEN** a retry marker already exists and new failures occur for the same month
- **THEN** the marker is updated to include all failed files (old + new) with updated timestamp.

### Requirement: Attendee Estimation Logic
Attendee counts and ID selection MUST follow the ranges and probability weighting defined in `config.toml`, allowing pure random sampling within bounds.

#### Scenario: Randomized scaling
- **WHEN** a transaction categorized as `会議費` or `接待費` is processed
- **THEN** the estimated attendee count is drawn randomly between the configured `min_attendees` (default 2) and `max_attendees` (default 8) from `config.toml` [processing] section, with optional amount-based weighting also defined in config; if no weighting is supplied the draw is uniformly random within the bounds.

#### Scenario: ID sampling
- **WHEN** attendee IDs are assigned per transaction
- **THEN** the pipeline uses weighted random selection: ID `2` has weight 0.9, ID `1` has weight 0.1 for the primary slot (configurable via `primary_id_weights` in config.toml), remaining slots are filled by sampling without replacement from the reference list, and the final list is padded with blanks up to `ID8` before sorting numerically.

#### Scenario: Configuration precedence
- **WHEN** both config.toml and environment variables define `min_attendees`
- **THEN** the CLI uses the value from the highest precedence source (CLI > env > config > pyproject) and logs which source was used.

### Requirement: Security and Data Hygiene
Sensitive transaction data MUST NOT be written to git-tracked locations or logs, and sanitized fixtures must back automated tests.

#### Scenario: Sanitized fixtures
- **WHEN** BDD scenarios run
- **THEN** they rely on `tests/data/` fixtures with anonymized values, and the CLI refuses to process files located under the repo path to avoid accidental commits.

#### Scenario: Repo-path validation
- **WHEN** a user passes `--input` pointing to a path inside the git repository
- **THEN** the CLI exits with error "Refusing to process files inside repository path. Use external directories." and status code 1.

#### Scenario: Sensitive data logging
- **WHEN** processing runs with verbose logging enabled
- **THEN** transaction amounts and store names are redacted in logs as `[REDACTED]`, and only summary statistics (count, total amount) are logged.

## ADDED Requirements

### Requirement: CSV Row Preservation
Processed CSVs MUST include ALL rows from the original CSV, with attendee columns populated only for relevant transactions.

#### Scenario: Non-relevant rows preserved
- **WHEN** a CSV contains 10 transactions: 6 with `会議費`/`接待費`, 4 with other categories
- **THEN** the processed CSV contains all 10 rows, with attendee columns (出席者, ID1-ID8) populated for the 6 relevant transactions and left blank for the 4 non-relevant rows.

#### Scenario: Column order consistency
- **WHEN** the processed CSV is written
- **THEN** it preserves the original column order, appending `出席者, ID1, ID2, ..., ID8` at the end.

#### Scenario: Original data integrity
- **WHEN** comparing original and processed CSVs
- **THEN** all original column values (利用日, ご利用店名及び商品名, 利用金額, 備考) remain unchanged for all rows.
