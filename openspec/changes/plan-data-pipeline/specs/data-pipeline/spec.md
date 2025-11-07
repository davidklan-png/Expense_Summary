## ADDED Requirements
### Requirement: Source Ingestion and Normalization
Business logic MUST first read credit CSV statements from `Input/` and reference files from `Reference/` as described in `docs/spec.txt`, then emit normalized CSV files before any HTML rendering occurs.

#### Scenario: Normalize before reporting
- **GIVEN** at least one CSV exists in `Input/` and reference metadata is available in `Reference/`
- **WHEN** the pipeline runs
- **THEN** it parses the sources, applies the attendee estimation rules, and writes a processed CSV per source into `Output/` using the original filename stem plus `.csv`.

### Requirement: CSV Parsing Rules
The pipeline MUST statically detect header rows, dynamically locate transaction rows, and tolerate encoding differences or missing columns per the spec.

#### Scenario: Header and encoding detection
- **WHEN** a CSV has headers offset or encoded in Shift_JIS/UTF-8
- **THEN** the parser locates the header row, auto-detects encoding, and loads rows without corrupting multibyte characters.

#### Scenario: Graceful degradation
- **WHEN** required columns (e.g., `備考`) are missing or a file is empty
- **THEN** the pipeline logs warnings, attempts to continue processing remaining files, and emits minimal placeholder reports rather than crashing.

### Requirement: HTML Rendering via Jinja2
After generating each processed CSV, the system MUST render an HTML report with the same filename stem using a Jinja2 template stored under `templates/`.

#### Scenario: Template-driven output
- **GIVEN** a processed file named `2024-01.csv`
- **WHEN** rendering completes
- **THEN** `Output/2024-01.html` is created via the configured Jinja2 template and contains the processed dataset plus attendee summaries per the spec.

### Requirement: Attendee Estimation Logic
Attendee counts and ID selection MUST follow the monetary thresholds and probability weighting defined in `docs/spec.txt`.

#### Scenario: Amount-based scaling
- **WHEN** a transaction categorized as `会議費` or `接待費` is processed
- **THEN** the estimated attendee count is at least 2, scales between 2–4 for amounts ≤10,000 JPY, and between 4–8 for larger amounts.

#### Scenario: ID sampling
- **WHEN** attendee IDs are assigned
- **THEN** ID "2" appears in 90% of qualifying transactions, "ID1" appears in the remaining 10%, selected IDs are sorted numerically, and no more than eight IDs are populated per row.

### Requirement: Test-First Workflow
All new functionality MUST be developed with both TDD unit tests and BDD acceptance specs written before implementation, maintaining overall coverage above 90%.

#### Scenario: Coverage gate
- **WHEN** the test suite runs (unit + BDD) in CI or locally
- **THEN** coverage reports show ≥90% line coverage, and changes that would drop coverage below the threshold are blocked until additional tests are added.

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
- **THEN** those values temporarily override the corresponding entries in `config.toml` for that invocation without persisting changes.

### Requirement: Output File Management
Generated files MUST respect source filename stems and append sequential suffixes if duplicates already exist.

#### Scenario: Duplicate outputs
- **WHEN** a processed CSV or HTML file name already exists in `Output/`
- **THEN** the system appends a numeric suffix (e.g., `_2`) before the extension to preserve previous artifacts.
