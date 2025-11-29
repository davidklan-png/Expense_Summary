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
- 🖥️ **Web Interface** - Interactive browser-based UI with drag-and-drop file upload, data editing, and network access

## Web Interface

The Saison Transform includes a user-friendly web interface built with Streamlit for processing files interactively.

### Starting the Web Interface

```bash
# Local access only (default)
./run_web.sh

# Access from other devices on your network
./run_web_network.sh
```

### Network Access (WSL2/Windows Users)

To access the web interface from other devices on your WiFi:

1. **Start the server in network mode:**
   ```bash
   ./run_web_network.sh
   ```

2. **Setup port forwarding (WSL2 only - first time setup):**

   Open PowerShell as Administrator on Windows and run:
   ```powershell
   # Option 1: Run the automated setup script
   cd path\to\saisonxform
   .\setup_port_forward.ps1

   # Option 2: Manual setup
   netsh interface portproxy add v4tov4 listenport=8502 listenaddress=0.0.0.0 connectport=8502 connectaddress=<WSL_IP>
   ```

3. **Find your Windows IP address:**
   ```powershell
   ipconfig
   # Look for "Wireless LAN adapter Wi-Fi" -> "IPv4 Address"
   # Example: 192.168.1.9
   ```

4. **Access from any device on your network:**
   - Open a browser on your phone, tablet, or another computer
   - Navigate to: `http://YOUR_WINDOWS_IP:8502`
   - Example: `http://192.168.1.9:8502`

### Features

- Drag & drop CSV file upload
- Interactive data editing with live preview
- Attendee management (add/edit/delete)
- Batch file processing
- Download all processed files as ZIP
- Real-time attendee count calculation

See [WEB_INTERFACE_GUIDE.md](docs/guides/WEB_INTERFACE_GUIDE.md) for detailed usage instructions.

## Directory Structure

Saison Transform uses a data directory structure within the project for easy access and persistence:

```
saisonxform/
├── data/
│   ├── input/                    # Upload CSV files here (via web interface)
│   ├── reference/                # Persistent configuration and reference data
│   │   ├── NameList.csv          # Attendee list (persists in git)
│   │   └── config.toml           # Configuration parameters (persists in git)
│   ├── output/                   # Processed CSV and HTML reports
│   └── archive/                  # Monthly archives of processed files
├── config.toml                   # Legacy config location (fallback)
└── web_app.py                    # Web interface
```

### Important Notes:

- **Input files**: Upload transaction CSV files through the web interface only
- **Reference folder**: Contains NameList.csv and config.toml which persist in git
- **Configuration**: Stored in `data/reference/config.toml` for persistence across sessions
- **Output/Archive**: Generated files are excluded from git (user data only)
- **Best Practice**: Always use the web interface for processing real data
- **Config Priority**: data/reference/config.toml → config.toml (root) → pyproject.toml defaults

## Quick Start

### Installation

**Requirements**: Python 3.10-3.13, Poetry

<details>
<summary>Installing Poetry (if not already installed)</summary>

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
</details>

#### Option 1: Global Installation (Recommended)

Install as a global command available system-wide:

```bash
# Install using pipx (recommended for CLI tools)
pipx install git+https://github.com/davidklan-png/Expense_Summary.git@develop

# Or install with pip (adds to user environment)
pip install --user git+https://github.com/davidklan-png/Expense_Summary.git@develop

# Verify installation
sf --version  # or: saisonxform --version

# Now you can use it directly without 'poetry run'
sf demo
sf --help
```

<details>
<summary>Installing pipx (if not already installed)</summary>

```bash
# macOS
brew install pipx
pipx ensurepath

# Ubuntu/Debian
sudo apt install pipx
pipx ensurepath

# Windows
py -m pip install --user pipx
py -m pipx ensurepath
```

**Why pipx?** Installs CLI tools in isolated environments while making them globally available.
</details>

#### Option 2: Clone Repository (For Development)

```bash
# 1. Clone repository
git clone git@github.com:davidklan-png/Expense_Summary.git saisonxform
cd saisonxform

# 2. Install dependencies with Poetry
poetry install

# 3. Verify installation
poetry run saisonxform --version
```

### Upgrading

Update to the latest version:

```bash
# If installed with pipx (recommended - automatically pulls latest from develop)
pipx upgrade saisonxform

# If installed with pip (automatically pulls latest from develop)
pip install --user --upgrade git+https://github.com/davidklan-png/Expense_Summary.git@develop

# Or install/upgrade to specific version tag
pip install --user --upgrade git+https://github.com/davidklan-png/Expense_Summary.git@v0.2.0

# If using Poetry (in project directory)
poetry update saisonxform
```

**Note**: Both `pipx upgrade saisonxform` and `pip install --user --upgrade git+https://...@develop` automatically fetch the latest code from the develop branch.

### Quick Test with Demo Files

After installation, try the demo to see how it works.

**Note**: Examples below use `sf` (short alias) for brevity. You can also use `saisonxform` - they're equivalent.

```bash
# Generate demo files (includes config.toml)
sf demo

# The demo creates:
# ./saisonxform-demo/
# ├── Input/202510_sample.csv     (5 sample transactions)
# ├── Reference/NameList.csv      (8 attendees)
# ├── Output/                     (results will be here)
# └── config.toml                 (auto-configured paths)

# Process the demo (cd into demo directory first)
cd saisonxform-demo
sf --verbose  # config.toml is auto-detected!

# Or run from outside with explicit paths
sf --input ./saisonxform-demo/Input \
   --reference ./saisonxform-demo/Reference \
   --output ./saisonxform-demo/Output \
   --verbose

# View the HTML report
open ./saisonxform-demo/Output/202510_sample.html
```

**💡 Tip**: The demo includes a `config.toml` file that auto-configures all paths. Just `cd` into the demo directory and run `sf`!

### Setup for Production Use

The project comes with a `data/` directory structure ready to use:

```bash
# 1. The directory structure is already created in data/
# data/input, data/reference, data/output, data/archive

# 2. Configuration and reference data are in data/reference/ (persisted in git)
# Verify or update them:
cat data/reference/NameList.csv      # Attendee list
cat data/reference/config.toml       # Configuration parameters

# 3. Use the web interface to upload and process files (recommended)
./run_web.sh           # Local access
./run_web_network.sh   # Network access

# 4. Or use CLI for batch processing
sf run --verbose
```

**Note**:
- The recommended workflow is to use the web interface for all real data processing
- Upload files through the web UI rather than manually copying to data/input/
- Configuration is stored in `data/reference/config.toml` and persists in git
- Edit config parameters in `data/reference/config.toml` to customize processing behavior

### Usage

```bash
# Process latest 2 months (default)
sf

# Process specific month(s)
sf --month 202510
sf --month 202510 --month 202511

# Force reprocess archived months
sf --month 202510 --force

# Verbose output
sf --verbose

# Override directories
sf --input /custom/input --output /custom/output
```

**Note**: If using Poetry development setup, prefix commands with `poetry run` (e.g., `poetry run sf`)

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

### Configuration Location

The configuration is stored in `data/reference/config.toml` and persists in git for consistency across sessions.

### Priority Order
1. Environment variables (highest)
2. Explicitly provided config file (`--config` option)
3. `data/reference/config.toml` (persistent configuration)
4. `config.toml` (project root fallback)
5. `pyproject.toml` (defaults, lowest)

### Amount-Based Attendee Estimation

The system supports two modes for determining attendee counts:

**Enabled (Default):** Attendee counts are determined by transaction amount using configurable brackets.
**Disabled:** Random selection between min_attendees and max_attendees.

Edit `data/reference/config.toml`:

```toml
[processing.amount_based_attendees]
enabled = true  # Set to false to disable amount-based logic

# Fallback calculation
cost_per_person = 3000

# Amount brackets (yen)
[processing.amount_based_attendees.brackets]
"0-5000" = { min = 2, max = 3 }        # Small transactions
"5001-15000" = { min = 3, max = 5 }    # Medium transactions
"15001-30000" = { min = 5, max = 8 }   # Large transactions
"30001-999999999" = { min = 6, max = 8 }  # Very large
```

**How it works:**
- When enabled: Matches transaction amount to bracket, randomly selects within bracket's min/max
- If no bracket matches: Calculates `amount / cost_per_person` (minimum 2)
- When disabled: Random selection between `min_attendees` and `max_attendees`

### Other Configuration Options

```toml
[paths]
input_dir = "data/input"
reference_dir = "data/reference"
output_dir = "data/output"
archive_dir = "data/archive"

[processing]
min_attendees = 2          # Used when amount-based is disabled
max_attendees = 8          # Also caps fallback calculations

[processing.primary_id_weights]
"2" = 0.9                  # 90% probability for ID '2'
"1" = 0.1                  # 10% probability for ID '1'
```

See [`data/reference/config.toml`](data/reference/config.toml) for full configuration with comments.

### Using Environment Variables

```bash
export INPUT_DIR=/custom/input
export REFERENCE_DIR=/custom/reference
export OUTPUT_DIR=/custom/output
export ARCHIVE_DIR=/custom/archive

poetry run sf run
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
<summary>"Command not found: sf" or "No module named 'saisonxform'"</summary>

**Solution 1**: Install globally with pipx (recommended)
```bash
pipx install git+https://github.com/davidklan-png/Expense_Summary.git@develop
sf --version  # Should work now
```

**Solution 2**: If using Poetry development setup, use `poetry run`
```bash
poetry run sf  # ✅ Correct
sf             # ❌ Wrong (not in PATH)
```

**Solution 3**: Activate Poetry environment
```bash
poetry shell
sf  # Now works within this shell
```
</details>

<details>
<summary>"Required directories not found"</summary>

Create directories outside repository:
```bash
cd ..
mkdir -p Input Reference Output
cd saisonxform
poetry run sf validate-config
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

- **[DEVELOPMENT.md](docs/development/DEVELOPMENT.md)** - Development phases and implementation details
- **[demo/README.md](demo/README.md)** - Demo usage instructions
- **[config.toml.example](config.toml.example)** - Configuration options
- **[CONTRIBUTING.md](docs/development/CONTRIBUTING.md)** - Contribution guidelines
- **[OpenSpec](openspec/)** - Technical specifications

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b add-feature`
3. Write tests first (TDD approach)
4. Maintain ≥87% test coverage
5. Use conventional commits: `feat:`, `fix:`, `test:`, `docs:`
6. Submit PR with clear description

See [CONTRIBUTING.md](docs/development/CONTRIBUTING.md) for details.

## License

[Specify your license]

## Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Docs**: [`docs/`](docs/) directory
- **Specs**: [`openspec/`](openspec/) directory
