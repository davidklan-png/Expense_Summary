## ADDED Requirements
### Requirement: Poetry Environment Baseline
The repository MUST use Poetry to manage dependencies for the `saisonxform` project name and keep the virtual environment outside the repo by default.

#### Scenario: Bootstrap project
- **GIVEN** a clean checkout
- **WHEN** a contributor runs `poetry install`
- **THEN** Poetry creates (or reuses) its default external virtualenv and installs declared dependencies, including `jinja2`, `pytest`, `pandas`, `numpy`, `chardet`, and Python's standard `random` module usage documented for clarity.

#### Scenario: Template awareness and validation
- **GIVEN** the project root
- **THEN** a `templates/` directory exists alongside `pyproject.toml`, and the bootstrap command fails fast with a descriptive error if the directory or required base template files (e.g., `templates/report.html.j2`) are missing.

### Requirement: Configurable External Data Folders
The application MUST reference four sibling folders—`Input/`, `Reference/`, `Output/`, and `Archive/`—via configuration stored in `config.toml` at the repository root using relative paths resolved from the repo directory, while also permitting absolute paths and environment-variable overrides.

- **GIVEN** `config.toml` contains entries `input_dir = "../Input"`, `reference_dir = "../Reference"`, `output_dir = "../Output"`, `archive_dir = "../Archive"`
- **WHEN** the CLI loads configuration
- **THEN** it resolves each path relative to the project root, verifies the directory exists outside the repo, and exposes the absolute paths to the business logic.

#### Scenario: Absolute paths and env overrides
- **WHEN** a user supplies absolute paths in `config.toml` or exports `INPUT_DIR`, `REFERENCE_DIR`, `OUTPUT_DIR`, or `ARCHIVE_DIR`
- **THEN** the CLI honors the environment variables first, then the explicit config values (relative or absolute), and finally falls back to `[tool.saisonxform]` entries in `pyproject.toml` if `config.toml` is absent.

#### Scenario: Folder purpose
- **GIVEN** the resolved directories
- **THEN** `Input/` stores raw credit CSV files, `Reference/` stores name lists and rule sheets, `Output/` receives generated CSV/HTML artifacts while remaining untracked by git, and `Archive/` stores month-specific subfolders of processed raw files.

### Requirement: Configuration Source of Truth
Runtime settings MUST have a single documented precedence order so contributors know whether to edit `config.toml` or `pyproject.toml`.

#### Scenario: Documented precedence
- **WHEN** onboarding documentation references configuration
- **THEN** it states the order `env vars` > `config.toml` > `pyproject.toml [tool.saisonxform]`, preventing duplication confusion.

### Requirement: CLI Skeleton Smoke Test
Phase 1 deliverables MUST include a no-op CLI skeleton (`saisonxform validate-config`) that loads configuration, verifies template presence, and exits with status code 0 without processing data.

#### Scenario: Dry-run validation
- **WHEN** `saisonxform validate-config --dry-run` is executed after Phase 1
- **THEN** it prints the resolved Input/Reference/Output paths, confirms template availability, and fails with a non-zero exit if any prerequisite is missing, ensuring environment issues are caught before Phase 2.
