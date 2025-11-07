# Saison Transform

Financial transaction processor for identifying meeting and entertainment expenses with automated attendee assignment.

## Features

- 🔍 **Smart Transaction Filtering** - Automatically identifies 会議費 (meeting) and 接待費 (entertainment) expenses
- 👥 **Attendee Estimation** - Estimates attendee count based on transaction amounts
- 🎲 **Weighted ID Assignment** - Assigns attendee IDs using configurable probability weights
- 📊 **Dual Output** - Generates both enhanced CSV and beautiful HTML reports
- 🗄️ **Auto-Archival** - Moves processed files to monthly archives automatically
- 🔐 **Security-First** - Prevents accidental data commits with git repository validation
- 🌐 **Encoding Detection** - Auto-detects UTF-8, UTF-8 BOM, and CP932/Shift-JIS encodings

## Quick Start

### Installation

```bash
# 1. Clone repository
git clone git@github.com:davidklan-png/Expense_Summary.git saisonxform
cd saisonxform

# 2. Install dependencies with Poetry
poetry install

# 3. Verify installation
poetry run saisonxform --version
```

**Requirements**: Python 3.10-3.13, Poetry

<details>
<summary>Installing Poetry</summary>

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
</details>

### Setup

```bash
# 1. Create directory structure (outside the repository)
cd ..
mkdir -p Input Reference Output

# Directory structure:
# Projects/
# ├── saisonxform/    # This repository
# ├── Input/          # CSV files to process
# ├── Reference/      # NameList.csv
# └── Output/         # Generated reports

# 2. Create attendee reference list
cat > Reference/NameList.csv << 'EOF'
ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
3,鈴木一郎,主任,DEF株式会社
EOF

# 3. Validate setup
cd saisonxform
poetry run saisonxform validate-config
```

### Usage

```bash
# Process latest 2 months (default)
poetry run saisonxform run

# Short alias
poetry run sf run

# Process specific month(s)
poetry run saisonxform run --month 202510
poetry run saisonxform run --month 202510 --month 202511

# Force reprocess archived months
poetry run saisonxform run --month 202510 --force

# Verbose output
poetry run saisonxform run --verbose

# Override directories
poetry run saisonxform run --input /custom/input --output /custom/output
```

**Expected Output:**
```
Found 1 CSV file(s) to process

Processing: 202510_transactions.csv
  • Encoding: utf-8
  • Relevant transactions: 15
  • CSV output: 202510_transactions.csv
  • HTML report: 202510_transactions.html
  • Archived to: Archive/202510/
  ✓ SUCCESS

============================================================
Processing complete:
  • Processed: 1  • Errors: 0  • Total: 1
============================================================
```

## Demo

See the [`demo/`](demo/) folder for complete examples:
- **Input**: Sample transaction CSV
- **Reference**: Sample NameList.csv
- **Output**: Processed CSV + HTML report

Run the demo:
```bash
# See demo/README.md for instructions
cat demo/README.md
```

## Input Format

### Transaction CSV

**Required columns:**
- `利用日` - Transaction date
- `ご利用店名及び商品名` - Store/merchant name
- `利用金額` - Amount (numeric)
- `備考` - Remarks (must contain `会議費` or `接待費`)

**Example:**
```csv
利用日,ご利用店名及び商品名,利用金額,備考
2025-10-01,東京レストラン,15000,会議費
2025-10-02,カフェABC,5000,接待費
2025-10-03,スーパー,3000,その他
```

**Features:**
- ✅ Header can be in first 10 rows
- ✅ Auto-encoding detection (UTF-8, CP932, Shift-JIS)
- ✅ Filename format: `YYYYMM_*.csv` (e.g., `202510_transactions.csv`)

### Reference CSV

**NameList.csv** with attendee information:

```csv
ID,Name,Title,Company
1,山田太郎,部長,ABC株式会社
2,佐藤花子,課長,XYZ株式会社
```

## Output Format

### Enhanced CSV

**ALL rows preserved** - including non-relevant transactions!

Added columns:
- `出席者` - Estimated attendee count
- `ID1` through `ID8` - Selected attendee IDs

**Example:**
```csv
利用日,ご利用店名及び商品名,利用金額,備考,出席者,ID1,ID2,ID3,...
2025-10-01,東京レストラン,15000,会議費,4,1,2,3,5
2025-10-02,カフェABC,5000,接待費,2,2,3,,
2025-10-03,スーパー,3000,その他,,,,,    ← Non-relevant row preserved
```

**Attendee Assignment Logic:**
- Count: Random between 2-8 (configurable)
- Primary ID: 90% ID '2', 10% ID '1' (configurable weights)
- Remaining: Random selection without replacement
- Sorted numerically, padded to ID8

### HTML Report

Beautiful report with:
- Transaction table with attendee details
- Unique attendee summary
- Total statistics

**Only includes relevant transactions** (会議費/接待費).

## Configuration

### Priority Order
1. CLI flags (highest)
2. Environment variables
3. `config.toml`
4. `pyproject.toml` (lowest)

### Using config.toml

Create `config.toml` in project root:

```toml
[paths]
input_dir = "../Input"
reference_dir = "../Reference"
output_dir = "../Output"
archive_dir = "../Archive"

[processing]
min_attendees = 2          # Minimum attendees
max_attendees = 8          # Maximum attendees

[processing.primary_id_weights]
"2" = 0.9                  # 90% probability
"1" = 0.1                  # 10% probability
```

See [`config.toml.example`](config.toml.example) for full configuration options.

### Using Environment Variables

```bash
export INPUT_DIR=/custom/input
export REFERENCE_DIR=/custom/reference
export OUTPUT_DIR=/custom/output
export ARCHIVE_DIR=/custom/archive

poetry run saisonxform run
```

## Archival Workflow

- ✅ **Per-file archival**: Each processed file moves to `Archive/YYYYMM/`
- ✅ **Retry markers**: Failed files create `.retry_YYYYMM.json`
- ✅ **Already-archived detection**: Prevents reprocessing without `--force`
- ✅ **Cross-filesystem support**: Copy+delete fallback

**Example:**
```
Archive/
├── 202510/
│   ├── 202510_transactions.csv
│   └── 202510_expenses.csv
├── 202511/
│   └── 202511_transactions.csv
└── .retry_202512.json    ← Partial failure marker
```

## Testing & Quality

**Test Coverage: 91%** (131 tests passing)

| Module | Coverage | Status |
|--------|----------|--------|
| config.py | 100% | ✅ Perfect |
| month_utils.py | 100% | ✅ Perfect |
| reporting.py | 100% | ✅ Perfect |
| selectors.py | 100% | ✅ Perfect |
| io.py | 95% | ✅ Excellent |
| cli.py | 81% | ✅ Excellent |

**Run tests:**
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=saisonxform --cov-report=html
open htmlcov/index.html

# Specific test
poetry run pytest tests/test_io.py -v
```

## Development

### Code Quality Tools

```bash
# Format code
poetry run black .
poetry run isort .

# Lint
poetry run ruff check .
poetry run ruff check --fix .

# Type check
poetry run mypy src/saisonxform

# Security scan
poetry run bandit -r src/saisonxform

# All quality checks
poetry run black . && poetry run isort . && poetry run ruff check . && poetry run mypy src/saisonxform
```

### Pre-commit Hooks

```bash
# Install hooks
poetry run pre-commit install

# Run on all files
poetry run pre-commit run --all-files
```

### CI/CD

GitHub Actions runs on all commits:
- ✅ Black formatting
- ✅ isort import sorting
- ✅ Ruff linting
- ✅ mypy type checking
- ✅ bandit security scan
- ✅ Tests on Python 3.10, 3.11, 3.12, 3.13
- ✅ Coverage reporting

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for configuration.

## Project Structure

```
saisonxform/
├── src/saisonxform/       # Main package
│   ├── cli.py             # CLI commands
│   ├── config.py          # Configuration
│   ├── io.py              # CSV I/O
│   ├── selectors.py       # Attendee logic
│   ├── reporting.py       # HTML reports
│   └── month_utils.py     # Archival utils
├── templates/             # Jinja2 templates
├── tests/                 # Test suite (122 tests)
├── demo/                  # Example files
├── docs/                  # Documentation
├── openspec/              # Specifications
├── config.toml.example    # Config template
└── pyproject.toml         # Dependencies
```

## Troubleshooting

<details>
<summary>"No module named 'saisonxform'"</summary>

Use `poetry run`:
```bash
poetry run saisonxform run  # ✅ Correct
saisonxform run             # ❌ Wrong
```

Or activate environment:
```bash
poetry shell
saisonxform run  # Now works
```
</details>

<details>
<summary>"Required directories not found"</summary>

Create directories outside repository:
```bash
cd ..
mkdir -p Input Reference Output
cd saisonxform
poetry run saisonxform validate-config
```
</details>

<details>
<summary>Encoding issues</summary>

Auto-detection fallback: UTF-8 BOM → UTF-8 → CP932

Convert if needed:
```bash
# macOS/Linux
iconv -f SHIFT-JIS -t UTF-8 input.csv > output.csv

# Check encoding
file -I input.csv
```
</details>

<details>
<summary>Git repository validation error</summary>

Data directories must be **outside** git repositories for security.

Move directories:
```bash
cd ..
mkdir -p Input Reference Output
# Update config.toml or use --input/--output flags
```
</details>

## Performance

**Expected on modern laptop (16GB RAM):**
- Processing: ~100 transactions/second
- Memory: <500MB
- Max file size: ~10,000 rows per CSV

## Documentation

- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Development phases and implementation details
- **[demo/README.md](demo/README.md)** - Demo usage instructions
- **[config.toml.example](config.toml.example)** - Configuration options
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[OpenSpec](openspec/)** - Technical specifications

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b add-feature`
3. Write tests first (TDD approach)
4. Maintain ≥87% test coverage
5. Use conventional commits: `feat:`, `fix:`, `test:`, `docs:`
6. Submit PR with clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[Specify your license]

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Docs**: [`docs/`](docs/) directory
- **Specs**: [`openspec/`](openspec/) directory
