## ADDED Requirements
### Requirement: Source Ingestion and Normalization
Business logic MUST first read credit CSV statements from `Input/` and reference files from `Reference/` as described in `docs/spec.txt`, then emit normalized CSV files before any HTML rendering occurs.

#### Scenario: Normalize before reporting
- **GIVEN** at least one CSV exists in `Input/` and reference metadata is available in `Reference/`
- **WHEN** the pipeline runs
- **THEN** it parses the sources, applies the attendee estimation rules, and writes a processed CSV per source into `Output/` using the original filename stem plus `.csv`.

### Requirement: CLI Architecture
The CLI MUST be implemented with Typer (or equivalent) to provide a `saisonxform` console script plus `sf` alias, supporting subcommands for `run` (default) and `validate-config`.

#### Scenario: Console script exposure
- **WHEN** Poetry installs the project
- **THEN** `pyproject.toml` defines two `console_scripts` entries—`saisonxform` and `sf`—both invoking the same Typer app that mirrors `python -m saisonxform.cli` behavior.

#### Scenario: Module parity
- **WHEN** a user runs `python -m saisonxform.cli run`
- **THEN** it executes the same code path as the console scripts, ensuring documentation references remain accurate.

#### Scenario: Subcommand clarity
- **WHEN** `saisonxform --help` is executed
- **THEN** it lists at least `run` (process files) and `validate-config` (checks config + directories) with consistent options.

### Requirement: CSV Parsing Rules
The pipeline MUST statically detect header rows, dynamically locate transaction rows, and tolerate encoding differences or missing columns per the spec.

#### Scenario: Header detection algorithm
- **WHEN** a CSV has headers on any of the first 10 rows
- **THEN** the parser scans line-by-line until it finds a row containing all required column titles (`利用日`, `ご利用店名及び商品名`, `利用金額`, `備考`), treats that row as the header, and treats the following row as the first transaction.

#### Scenario: Encoding detection and fallback
- **WHEN** chardet returns a low confidence (<0.6) or fails to detect encoding
- **THEN** the pipeline attempts `utf-8-sig`, `utf-8`, and `cp932` in order, logging the encoding actually used; mixed encodings within one file trigger a warning and result in UTF-8 output.

#### Scenario: Graceful degradation
- **WHEN** required columns (e.g., `備考`) are missing or a file is empty
- **THEN** the pipeline logs warnings, attempts to continue processing remaining files, and emits minimal placeholder reports rather than crashing.

### Requirement: HTML Rendering via Jinja2
After generating each processed CSV, the system MUST render an HTML report with the same filename stem using a Jinja2 template stored under `templates/`.

#### Scenario: Template-driven output
- **GIVEN** a processed file named `2024-01.csv`
- **WHEN** rendering completes
- **THEN** `Output/2024-01.html` is created via the configured Jinja2 template and contains the processed dataset plus attendee summaries per the spec.

#### Scenario: Template contract
- **WHEN** rendering executes
- **THEN** the template receives a context object containing `statement_meta`, `transactions` (list of dicts with attendee columns), and `unique_attendees`, and the template includes placeholders for these keys; missing placeholders cause a startup validation error.

### Requirement: Output Schema Consistency
Processed CSVs MUST add separate columns `出席者`, `ID1` through `ID8`, leaving blank strings when fewer IDs exist, and HTML reports MUST display the same information.

#### Scenario: Sparse attendees
- **WHEN** only three attendees are selected
- **THEN** `ID4`–`ID8` are emitted as empty fields in the CSV, and the HTML shows only populated IDs without introducing placeholder text.

### Requirement: Attendee Estimation Logic
Attendee counts and ID selection MUST follow the ranges and probability weighting defined in `config.toml`, allowing pure random sampling within bounds.

#### Scenario: Randomized scaling
- **WHEN** a transaction categorized as `会議費` or `接待費` is processed
- **THEN** the estimated attendee count is drawn randomly between the configured `min_attendees` (default 2) and `max_attendees` (default 8), with optional amount-based weighting also defined in config; if no weighting is supplied the draw is uniformly random within the bounds.

#### Scenario: ID sampling
- **WHEN** attendee IDs are assigned per transaction
- **THEN** the pipeline uses weighted random selection: ID `2` has weight 0.9, ID `1` has weight 0.1 for the primary slot, remaining slots are filled by sampling without replacement from the reference list according to weights defined in `config.toml`, and the final list is padded with blanks up to `ID8` before sorting numerically.

### Requirement: Test-First Workflow
All new functionality MUST be developed with both TDD unit tests and BDD acceptance specs written before implementation, maintaining overall coverage above 90%.

#### Scenario: Coverage gate
- **WHEN** the test suite runs (unit + BDD) in CI or locally
- **THEN** coverage reports show ≥90% line coverage for the entire `saisonxform` package, and changes that would drop coverage below the threshold are blocked until additional tests are added.

#### Scenario: Tests precede implementation
- **WHEN** a new pipeline capability is introduced
- **THEN** the corresponding unit specs and BDD scenarios are authored (and initially fail) before production code for that capability is merged.

### Requirement: CLI Invocation and Month Selection
The project MUST expose a console script named `saisonxform` (alias `sf`) that accepts configuration overrides and month filters for processing.

#### Scenario: Explicit month arguments
- **GIVEN** a user runs `saisonxform run --config config.toml --month 202510 --month 202511`
- **THEN** only data for the specified year-month pairs is processed, and Input/Reference/Output paths come from the provided config (unless overridden by `--input/--reference/--output`).

#### Scenario: Default month window
- **GIVEN** no `--month` arguments are supplied
- **WHEN** the command executes
- **THEN** it automatically selects the latest two months relative to the current date and processes only those statements.

#### Scenario: Path overrides
- **WHEN** a user passes `--input`, `--reference`, or `--output` on the CLI
- **THEN** those values temporarily override the corresponding entries in `config.toml` for that invocation without persisting changes, and the precedence order (CLI > env vars > config > pyproject) is logged once per run.

### Requirement: Output File Management
Generated files MUST respect source filename stems and append sequential suffixes if duplicates already exist.

#### Scenario: Duplicate outputs
- **WHEN** a processed CSV or HTML file name already exists in `Output/`
- **THEN** the system appends a numeric suffix (e.g., `_2`) before the extension to preserve previous artifacts.

### Requirement: Month Selection
Default month processing MUST operate on filename prefixes shaped as `YYYYMM*`, with fallback to explicit CLI months.

#### Scenario: Filename-based detection
- **WHEN** no `--month` flag is supplied
- **THEN** the CLI enumerates files in `Input/`, identifies those whose names start with `YYYYMM`, sorts them descending, and processes only the latest two distinct months.

#### Scenario: Mixed naming patterns
- **WHEN** files do not match the `YYYYMM` pattern
- **THEN** the CLI logs a warning and skips them unless explicit `--month` flags were provided that match the ambiguous files.

### Requirement: Post-Processing Archival
After successfully processing individual CSVs, each raw file MUST be moved from `Input/` to the configured `Archive/` directory to prevent reprocessing; the `Archive/` directory is auto-created if it does not exist.

#### Scenario: Per-file archival granularity
- **WHEN** a file (e.g., `202510_A.csv`) is successfully processed
- **THEN** that specific file is immediately moved to `Archive/202510/202510_A.csv`, creating both `Archive/` and the month subdirectory if needed, independent of whether other files in the same month succeed or fail.

#### Scenario: Partial month processing
- **WHEN** processing month `202510` with 5 input files, where 4 succeed and 1 fails
- **THEN** the 4 successful files are archived to `Archive/202510/`, the 1 failed file remains in `Input/`, and a retry marker file `Archive/.retry_202510.json` is created containing `{"month": "202510", "failed_files": ["202510_E.csv"], "error": "..."}`.

#### Scenario: Already-archived month detection
- **WHEN** a user explicitly requests `--month 202510` and `Archive/202510/` exists without a retry marker
- **THEN** the CLI exits immediately with error status and message "Month 202510 already processed. Use --force to reprocess." without scanning `Input/`.

#### Scenario: Force reprocessing
- **WHEN** a user passes `--month 202510 --force` and archived files exist
- **THEN** the CLI processes any matching files found in `Input/`, archives them per normal flow, and logs a warning that this may create duplicate outputs.

#### Scenario: Archive directory auto-creation
- **WHEN** the first archival operation runs and `Archive/` does not exist
- **THEN** the CLI creates `Archive/` at the configured path (relative or absolute), logs the creation, and proceeds with archival.

#### Scenario: Archive failure handling
- **WHEN** archival fails for a file (e.g., permissions, disk full, cross-filesystem move error)
- **THEN** the CLI emits an error, creates/updates the retry marker file `Archive/.retry_YYYYMM.json` with failure details, leaves the unarchived file in `Input/`, and exits with non-zero status so operators can intervene before rerunning.

### Requirement: Retry Marker Format
Retry marker files MUST be JSON documents stored as `Archive/.retry_YYYYMM.json` containing structured failure information for operator intervention.

#### Scenario: Marker file structure
- **WHEN** a retry marker is created for month `202510`
- **THEN** the file `Archive/.retry_202510.json` contains at minimum: `{"month": "202510", "failed_files": ["filename1.csv", ...], "timestamp": "ISO8601", "errors": [{"file": "filename1.csv", "error": "error message"}]}`.

#### Scenario: Marker cleanup on success
- **WHEN** all previously failed files in a month are successfully processed and archived
- **THEN** the corresponding `.retry_YYYYMM.json` file is deleted, signaling full completion.

### Requirement: Performance and Scalability
The pipeline MUST handle at least 50 CSV files of up to 10,000 rows each within 5 minutes on a modern laptop (16GB RAM), keeping resident memory under 500MB.

#### Scenario: Performance benchmark
- **WHEN** integration tests run with synthetic datasets
- **THEN** aggregate processing time and memory usage are recorded, and alerts trigger if thresholds are exceeded.

### Requirement: Security and Data Hygiene
Sensitive transaction data MUST NOT be written to git-tracked locations or logs, and sanitized fixtures must back automated tests.

#### Scenario: Sanitized fixtures
- **WHEN** BDD scenarios run
- **THEN** they rely on `tests/data/` fixtures with anonymized values, and the CLI refuses to process files located under the repo path to avoid accidental commits.

### Requirement: Acceptance Examples
The repository MUST include canonical input/output pairs demonstrating expected attendee counts and HTML structure.

#### Scenario: Golden fixtures
- **WHEN** developers run `pytest -m acceptance`
- **THEN** golden files validate that a known input (e.g., `tests/data/sample_202510.csv`) produces the documented CSV + HTML output stored under `tests/data/expected/`.
