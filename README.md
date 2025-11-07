# Saison Transform

Financial transaction processor for identifying meeting and entertainment expenses with automated attendee assignment.

## Overview

Saison Transform processes credit card CSV files to:
- Identify 會議費 (meeting expenses) and 接待費 (entertainment expenses)
- Estimate attendee counts based on transaction amounts
- Assign attendee IDs from a reference list using weighted sampling
- Generate both CSV and HTML reports

## Status

**Current Phase**: Phase 1 (CLI Migration) Complete ✅
**Test Coverage**: 54% (CLI code not yet tested - Phase 7 pending)
**Tests Passing**: 54 passed, 8 skipped

### ✅ Phase 1: Environment Setup (Complete)
- Poetry-based dependency management
- Configuration system (config.toml + environment variables)
- Project structure and packaging
- **NEW**: Typer-based CLI with `run` and `validate-config` commands
- **NEW**: `sf` command alias for convenience
- Jinja2 templates for HTML reporting

### ✅ Phase 2: Data Pipeline (Complete)
- CSV processing with auto-encoding detection
- Transaction filtering and attendee estimation
- ID sampling with configurable weights (90% ID '2', 10% ID '1')
- HTML report generation
- ≥90% test coverage achieved (91.55%)

### 🚧 In Progress: CLI Enhancement & Archival
- Month filtering (--month, default to latest 2 months)
- Archival workflow (move files to Archive/YYYYMM/)
- CSV row preservation (keep all rows, not just filtered)
- Configuration integration (attendee settings from config.toml)
- Security validation (repo-path checking, precedence logging)

## Quick Start

### 1. Prerequisites

- **Python 3.10 - 3.13**
- **Poetry** (dependency management)

Install Poetry if you haven't already:
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 2. Installation

```bash
# Clone repository
git clone <repository-url>
cd saisonxform

# Install dependencies with Poetry
poetry install

# Verify installation
poetry run saisonxform
```

Expected output:
```
Usage: saisonxform [OPTIONS] COMMAND [ARGS]...

Financial Transaction Processor - Process credit card statements and assign attendees

Options:
  --version  Show version and exit
  --help     Show this message and exit.

Commands:
  run              Process transaction CSV files from Input directory.
  validate-config  Validate configuration and check directory setup.
```

### 3. Setup Directories

Create the required directory structure:

```bash
# Navigate to parent directory of saisonxform
cd ..

# Create required directories
mkdir -p Input Reference Output

# Directory structure should look like:
# Projects/
# ├── saisonxform/    # This repo
# ├── Input/          # Place CSV files here
# ├── Reference/      # Place NameList.csv here
# └── Output/         # Generated reports go here
```

### 4. Prepare Reference Data

Create `Reference/NameList.csv` with attendee information:

```csv
ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
3,鈴木一郎,主任,DEF株式会社
4,田中美咲,係長,GHI株式会社
5,高橋健太,社員,JKL株式会社
```

### 5. Validate Setup

```bash
cd saisonxform
poetry run saisonxform validate-config
```

Expected output:
```
Validating configuration...

Input directory:     /path/to/Input
Reference directory: /path/to/Reference
Output directory:    /path/to/Output
Archive directory:   /path/to/Archive

Checking directories...
✓ All required directories exist

Checking templates...
✓ All required templates exist

============================================================
Configuration validation complete - SUCCESS
============================================================
```

### 6. Process CSV Files

Place your transaction CSV files in the `Input/` directory, then:

```bash
# Process all CSV files
poetry run saisonxform run

# Or use the short alias
poetry run sf run

# Process specific month(s)
poetry run saisonxform run --month 202510

# Process with verbose output
poetry run saisonxform run --verbose

# Override directories for a specific run
poetry run saisonxform run --input /path/to/custom/input
```

Expected output:
```
Found 1 CSV file(s) to process

Processing: 202510_transactions.csv
  - Detected encoding: utf-8
  - Found 15 relevant transactions
  - CSV output: 202510_transactions.csv
  - HTML report: 202510_transactions.html
  ✓ SUCCESS

============================================================
Processing complete:
  - Processed: 1
  - Errors: 0
  - Total: 1
============================================================
```

## Configuration

### Configuration Priority

The application loads configuration in this order (highest to lowest):
1. **Environment variables** (`INPUT_DIR`, `REFERENCE_DIR`, `OUTPUT_DIR`, `ARCHIVE_DIR`)
2. **config.toml** in project root
3. **pyproject.toml** `[tool.saisonxform]` section

### Using Environment Variables

```bash
# Set custom directories via environment variables
export INPUT_DIR=/custom/path/to/input
export REFERENCE_DIR=/custom/path/to/reference
export OUTPUT_DIR=/custom/path/to/output
export ARCHIVE_DIR=/custom/path/to/archive

# Run with custom paths
poetry run saisonxform run
```

### Using config.toml

Create `config.toml` in project root:

```toml
[paths]
input_dir = "../Input"
reference_dir = "../Reference"
output_dir = "../Output"
archive_dir = "../Archive"
```

## Input Data Format

### Transaction CSV Requirements

Your CSV files must contain these columns:
- **利用日** - Transaction date (any format)
- **ご利用店名及び商品名** - Store name and product description
- **利用金額** - Transaction amount (numeric)
- **備考** - Remarks (must contain '会議費' or '接待費' to be processed)

Example:
```csv
利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,東京レストラン,15000,会議費
2025-10-02,カフェABC,5000,接待費
2025-10-03,スーパーマーケット,3000,その他
```

**Notes:**
- Header row can be anywhere in the first 10 rows
- Encoding is auto-detected (supports UTF-8, UTF-8 BOM, CP932/Shift-JIS)
- Only transactions with '会議費' or '接待費' in 備考 are processed

### NameList.csv Requirements

Reference file for attendee information:
- **ID** - Unique attendee identifier (numeric string)
- **Name** - Attendee name
- **Title** - Job title
- **Company** - Company name

## Output Format

### Processed CSV

The output CSV includes original columns plus:
- **出席者** - Estimated attendee count (2-8, randomly assigned)
- **ID1** through **ID8** - Selected attendee IDs (from NameList.csv)

Example:
```csv
利用日,ご利用店名及び商品名,利用金額,備考,出席者,ID1,ID2,ID3,ID4,ID5,ID6,ID7,ID8
2025-10-01,東京レストラン,15000,会議費,4,1,2,3,5,,,,
2025-10-02,カフェABC,5000,接待費,2,2,3,,,,,
```

**Attendee Assignment Logic:**
- Count: Random between 2-8 attendees per transaction
- Primary ID: 90% chance of ID '2', 10% chance of ID '1'
- Remaining IDs: Random selection without replacement
- Sorted numerically, padded with empty strings to ID8

### HTML Report

Beautiful HTML report includes:
- **Transaction Table**: All processed transactions with attendee assignments
- **Unique Attendee List**: Details of all attendees selected across transactions
- **Summary Statistics**: Total transactions, total amount, attendee count

## Code Quality & CI/CD

This project enforces strict code quality standards through automated tooling:

### Quick Commands

```bash
# Install pre-commit hooks (run once)
make pre-commit-install

# Format code (black + isort)
make format

# Run linter (ruff)
make lint

# Run all quality checks
make qa

# Simulate CI checks locally
make ci
```

### Available Tools

- **Black**: Code formatting (120 char line length)
- **isort**: Import sorting
- **Ruff**: Fast Python linter (replaces flake8, pylint, pyupgrade, etc.)
- **mypy**: Static type checking
- **bandit**: Security vulnerability scanner
- **pytest**: Testing framework with coverage

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality:

```bash
# Install hooks
poetry run pre-commit install

# Run manually on all files
poetry run pre-commit run --all-files
```

Hooks include: formatting, linting, type checking, security scanning, and commit message validation.

### CI Pipeline

GitHub Actions runs on all pushes and pull requests:
- ✅ Code formatting (black, isort)
- ✅ Linting (ruff)
- ✅ Type checking (mypy)
- ✅ Security scan (bandit)
- ✅ Tests on Python 3.10, 3.11, 3.12, 3.13
- ✅ Coverage reporting to Codecov

See `.github/workflows/ci.yml` for full pipeline configuration.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines, code style requirements, and PR submission process.

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run with coverage report
poetry run pytest --cov=saisonxform --cov-report=html

# Run specific test file
poetry run pytest tests/test_io.py

# Run tests matching a pattern
poetry run pytest -k "test_filter"
```

View coverage report:
```bash
# Generate HTML coverage report
poetry run pytest --cov=saisonxform --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Open in browser (Linux)
xdg-open htmlcov/index.html

# Open in browser (Windows)
start htmlcov/index.html
```

### Code Quality Tools

```bash
# Format code with Black (line length: 120)
poetry run black . --line-length 120

# Sort imports with isort
poetry run isort .

# Lint code with Ruff
poetry run ruff check .

# Auto-fix linting issues
poetry run ruff check --fix .

# Run all formatters at once
poetry run black . && poetry run isort . && poetry run ruff check --fix .
```

### Project Structure

```
saisonxform/
├── src/saisonxform/          # Main package
│   ├── __init__.py           # Package metadata
│   ├── config.py             # Configuration management
│   ├── cli.py                # CLI entry point
│   ├── io.py                 # CSV I/O with encoding detection
│   ├── selectors.py          # Attendee estimation and ID sampling
│   └── reporting.py          # HTML report generation
├── templates/                 # Jinja2 templates
│   └── report.html.j2        # HTML report template
├── tests/                     # Test suite (91.55% coverage)
│   ├── data/                 # Test fixtures
│   ├── test_io.py            # I/O tests (11 tests)
│   ├── test_selectors.py     # Selector tests (16 tests)
│   ├── test_reporting.py     # Reporting tests (13 tests)
│   ├── test_integration.py   # Integration tests (11 tests)
│   └── test_edge_cases.py    # Edge case tests (11 tests)
├── docs/                      # Documentation
│   ├── spec.txt              # Original requirements
│   └── NameList.csv          # Sample reference data
├── openspec/                  # OpenSpec specifications
│   ├── specs/                # Capability specifications
│   └── changes/              # Change proposals
│       └── plan-data-pipeline/ # Phase 2 implementation
│           ├── proposal.md   # Why and what
│           ├── tasks.md      # Implementation checklist
│           ├── evidence.md   # Completion proof
│           └── specs/        # Delta specifications
├── config.toml               # Default configuration
├── pyproject.toml            # Poetry dependencies and project config
├── README.md                 # This file
└── CLAUDE.md                 # AI assistant instructions
```

### Adding New Features

This project follows OpenSpec specification-driven development:

1. **Check existing specs**:
   ```bash
   openspec list --specs
   openspec list
   ```

2. **Create change proposal**:
   ```bash
   mkdir -p openspec/changes/add-new-feature
   # Create proposal.md, tasks.md, and spec deltas
   ```

3. **Validate proposal**:
   ```bash
   openspec validate add-new-feature --strict
   ```

4. **Implement with TDD**:
   - Write failing tests first
   - Implement feature to pass tests
   - Maintain ≥90% coverage

5. **Archive when complete**:
   ```bash
   openspec archive add-new-feature --yes
   ```

## Troubleshooting

### "No module named 'saisonxform'"

Make sure you're running commands with `poetry run`:
```bash
poetry run saisonxform run  # Correct
saisonxform run             # Wrong - won't find the module
```

Or activate the virtual environment:
```bash
poetry shell
saisonxform run  # Now it works
```

### "Required directories not found"

Ensure Input, Reference, and Output directories exist:
```bash
cd ..  # Go to parent directory
mkdir -p Input Reference Output
ls -la  # Verify they exist
```

### "NameList.csv not found"

Create the reference file:
```bash
cat > Reference/NameList.csv << 'EOF'
ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
EOF
```

### Encoding Issues

The application auto-detects encoding with fallback chain:
1. UTF-8 with BOM (utf-8-sig)
2. UTF-8 (utf-8)
3. CP932/Shift-JIS (cp932)

If you have encoding issues, try:
```bash
# Convert to UTF-8 (macOS/Linux)
iconv -f SHIFT-JIS -t UTF-8 input.csv > input_utf8.csv

# Check file encoding
file -I input.csv
```

### Tests Failing

```bash
# Run tests with verbose output to see failures
poetry run pytest -vv

# Run only failing tests
poetry run pytest --lf

# Run with detailed output
poetry run pytest -vv --tb=short
```

## Performance

Expected performance on a modern laptop (16GB RAM):
- **Processing Speed**: ~100 transactions/second
- **Memory Usage**: <500MB for typical workloads
- **File Size**: Handles up to 10,000 rows per CSV

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b add-new-feature`
3. Follow TDD approach (write tests first)
4. Ensure ≥90% test coverage
5. Use conventional commits: `feat:`, `fix:`, `test:`, `docs:`
6. Submit pull request with evidence.md

## License

[Specify your license here]

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: See `docs/` directory
- **Specifications**: See `openspec/` directory

## References

- **OpenSpec Framework**: Specification-driven development
- **Poetry Documentation**: https://python-poetry.org/docs/
- **Test Coverage Report**: Run `poetry run pytest --cov=saisonxform --cov-report=html`
