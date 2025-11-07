## ADDED Requirements
### Requirement: Poetry Environment Baseline
The repository MUST use Poetry to manage dependencies for the `saisonxform` project name and keep the virtual environment outside the repo by default.

#### Scenario: Bootstrap project
- **GIVEN** a clean checkout
- **WHEN** a contributor runs `poetry install`
- **THEN** Poetry creates (or reuses) its default external virtualenv and installs declared dependencies, limited at minimum to `jinja2` and `pytest` until additional libraries are justified.

#### Scenario: Template awareness
- **GIVEN** the project root
- **THEN** a `templates/` directory exists alongside `pyproject.toml` so Jinja2 templates can be committed with the codebase.

### Requirement: Configurable External Data Folders
The application MUST reference three sibling folders—`Input/`, `Reference/`, `Output/`—via a `config.toml` file at the repository root using relative paths resolved from the repo directory.

#### Scenario: Config resolution
- **GIVEN** `config.toml` contains entries `input_dir = "../Input"`, `reference_dir = "../Reference"`, `output_dir = "../Output"`
- **WHEN** the CLI loads configuration
- **THEN** it resolves each path relative to the project root, verifies the directory exists outside the repo, and exposes the absolute paths to the business logic without requiring environment variables.

#### Scenario: Folder purpose
- **GIVEN** the resolved directories
- **THEN** `Input/` stores raw credit CSV files, `Reference/` stores name lists and rule sheets, and `Output/` receives generated CSV/HTML artifacts while remaining untracked by git.
