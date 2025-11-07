# Saison Transform

Financial transaction processor for identifying meeting and entertainment expenses with automated attendee assignment.

## Overview

Saison Transform processes credit card CSV files to:
- Identify 會議費 (meeting expenses) and 接待費 (entertainment expenses)
- Estimate attendee counts based on transaction amounts
- Assign attendee IDs from a reference list using weighted sampling
- Generate both CSV and HTML reports

## Status

**Current Phase**: Phase 1 Complete ✅
**Next Phase**: Phase 2 (Data Pipeline Implementation)

### Phase 1: Environment Setup (Complete)
- ✅ Poetry-based dependency management
- ✅ Configuration system (config.toml + environment variables)
- ✅ Project structure and packaging
- ✅ CLI skeleton with `validate-config` command
- ✅ Jinja2 templates for HTML reporting

### Phase 2: Data Pipeline (Planned)
- CSV processing with auto-encoding detection
- Transaction filtering and attendee estimation
- ID sampling with configurable weights
- HTML report generation
- Archival workflow with retry markers
- ≥90% test coverage

## Installation

### Prerequisites
- Python 3.10 - 3.13
- Poetry (for dependency management)

### Setup
```bash
# Clone repository
git clone <repository-url>
cd saisonxform

# Install dependencies
poetry install

# Verify installation
poetry run saisonxform validate-config
```

## Configuration

Configuration precedence (highest to lowest):
1. Environment variables (`INPUT_DIR`, `REFERENCE_DIR`, `OUTPUT_DIR`, `ARCHIVE_DIR`)
2. `config.toml` in project root
3. `pyproject.toml` [tool.saisonxform] section

### External Directories

The application expects four sibling directories (configured in `config.toml`):

```toml
[paths]
input_dir = "../Input"        # Raw CSV files (must pre-exist)
reference_dir = "../Reference" # NameList.csv and rules (must pre-exist)
output_dir = "../Output"       # Generated reports (must pre-exist)
archive_dir = "../Archive"     # Processed files by month (auto-created)
```

**Directory Layout**:
```
Projects/
├── saisonxform/          # This repository
│   ├── src/
│   ├── templates/
│   ├── config.toml
│   └── pyproject.toml
├── Input/                # Raw CSV files
├── Reference/            # NameList.csv
├── Output/               # Generated CSV/HTML
└── Archive/              # Processed files
    ├── 202510/
    └── 202511/
```

## Usage

### Phase 1 Commands

```bash
# Validate configuration and directory setup
poetry run saisonxform validate-config

# Show help
poetry run saisonxform
```

### Phase 2 Commands (Coming Soon)

```bash
# Process all files in Input directory
poetry run saisonxform process

# Process specific month
poetry run saisonxform process --month 202510

# Force reprocess already-processed month
poetry run saisonxform process --month 202510 --force
```

## Development

### Project Structure

```
saisonxform/
├── src/saisonxform/          # Main package
│   ├── __init__.py          # Package metadata
│   ├── config.py            # Configuration management
│   ├── cli.py               # CLI entry point
│   ├── io.py                # CSV I/O (Phase 2)
│   ├── selectors.py         # Attendee logic (Phase 2)
│   └── reporting.py         # HTML generation (Phase 2)
├── templates/                # Jinja2 templates
│   └── report.html.j2
├── tests/                    # Test suite
│   ├── data/                # Test fixtures
│   └── test_*.py            # Unit tests
├── docs/                     # Specifications
│   ├── spec.txt             # Requirements
│   └── NameList.csv         # Sample data
├── openspec/                 # OpenSpec proposals
│   ├── specs/               # Capability specs
│   └── changes/             # Change proposals
├── config.toml              # Default configuration
└── pyproject.toml           # Poetry & project config
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=saisonxform --cov-report=html

# Run specific test file
poetry run pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check --fix .
```

## OpenSpec Workflow

This project uses OpenSpec for specification-driven development.

### Before Making Changes

```bash
# List all specs and active proposals
openspec list --specs
openspec list

# View specific proposal
openspec show <change-id>

# Search specifications
rg -n "Requirement:|Scenario:" openspec/specs
```

### Creating Change Proposals

1. Review existing specs: `openspec list --specs`
2. Create proposal directory: `openspec/changes/<change-id>/`
3. Create required files:
   - `proposal.md` - Why, what, impact
   - `tasks.md` - Implementation checklist
   - `specs/<capability>/spec.md` - Delta specs
4. Validate: `openspec validate <change-id> --strict`
5. Get approval before implementing
6. Archive when complete: `openspec archive <change-id> --yes`

## Input Data Format

### Transaction CSV
Required columns:
- **利用日** - Transaction date
- **ご利用店名及び商品名** - Store name and product
- **利用金額** - Transaction amount (numeric)
- **備考** - Remarks (must contain '会議費' or '接待費')

### NameList.csv (Reference)
Required columns:
- **ID** - Unique attendee identifier
- **Name** - Attendee name
- **Title** - Job title
- **Company** - Company name

## Output Format

### Processed CSV
Original columns plus:
- **出席者** - Estimated attendee count (2-8)
- **ID1** through **ID8** - Selected attendee IDs

### HTML Report
Includes:
- Transaction table with attendee assignments
- Unique attendee list with details
- Processing metadata and statistics

## Contributing

1. Check OpenSpec proposals: `openspec list`
2. Review specifications in `docs/spec.txt`
3. Follow TDD/BDD approach (tests first)
4. Target ≥90% test coverage
5. Use conventional commits: `feat:`, `fix:`, `test:`, `docs:`
6. Update `tasks.md` checklist as you work
7. Create evidence.md when complete

## License

[Specify your license here]

## References

- **Specifications**: `docs/spec.txt`
- **OpenSpec Proposals**: `openspec/changes/`
- **Configuration Guide**: `CLAUDE.md`
- **Agent Guide**: `AGENTS.md`
