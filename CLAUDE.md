# Saison Transform - Project Context

## Overview

**Saison Transform** is a financial transaction processor for identifying meeting and entertainment expenses with automated attendee assignment. It processes Japanese credit card CSV files, identifies 會議費 (meeting expenses) and 接待費 (entertainment expenses), estimates attendee counts, and generates CSV/HTML reports.

- **Language**: Python 3.10-3.13
- **Package Manager**: Poetry
- **Web UI**: Streamlit
- **Testing**: pytest with 91% coverage target (145+ tests)

## Project Structure

```
saisonxform/
├── src/saisonxform/           # Main Python package
│   ├── cli.py                 # CLI commands (sf, saisonxform)
│   ├── config.py              # Configuration management
│   ├── io.py                  # CSV I/O with encoding detection
│   ├── selectors.py           # Attendee estimation & ID sampling logic
│   ├── reporting.py           # HTML report generation
│   └── month_utils.py         # Archival utilities
├── web_app.py                 # Streamlit web interface
├── tests/                     # Test suite (145+ tests)
├── data/                      # Runtime data (NOT in git)
│   ├── input/                # Uploaded CSV files (via web UI)
│   ├── reference/             # Reference data (in git)
│   │   ├── NameList.csv      # Attendee reference list (with Core column)
│   │   └── config.toml       # Configuration parameters
│   ├── output/               # Generated reports
│   └── archive/              # Monthly archives (Archive/YYYYMM/)
├── templates/                 # Jinja2 templates for HTML reports
├── demo/                     # Demo/example files
└── docs/                     # Documentation
```

## Key Commands

```bash
# Install dependencies
poetry install

# Run CLI
poetry run sf --help
poetry run saisonxform process --input file.csv

# Run web interface
poetry run streamlit run web_app.py

# Run tests
poetry run pytest
poetry run pytest --cov

# Code quality
poetry run black src tests
poetry run ruff check src tests
poetry run mypy src
poetry run bandit -r src
```

## Core Functionality

### 1. Transaction Processing
- Reads credit card CSV files with Japanese transaction data
- Identifies expenses by category (會議費, 接待費)
- Estimates attendee counts based on transaction amount brackets
- Assigns attendee IDs from NameList.csv reference

### 2. Encoding Handling
- Auto-detection chain: UTF-8 BOM → UTF-8 → CP932/Shift-JIS
- Output always UTF-8 with BOM

### 3. Core Member ID Assignment (v0.4.0+)
- **Core Members** (Core=1 in NameList.csv): Prioritized in attendee selection
- **Non-Core Members** (Core=0): Available during manual editing
- Core fill strategy: "random" (default) or "sequential"
- Output padded to ID8, sorted numerically
- **Legacy Mode**: Falls back to weighted ID assignment if no Core column

### 4. Configuration Precedence (highest to lowest)
1. Environment variables
2. Explicit `--config` file
3. `data/reference/config.toml` (persistent)
4. `config.toml` (project root fallback)
5. `pyproject.toml` defaults

### 5. Dual Interface
- **CLI**: `sf`/`saisonxform` commands for batch processing
- **Web**: Streamlit app with drag-drop upload, interactive editing, 3-step workflow

## Development Patterns

### Testing
- TDD/BDD approach required
- 145+ tests passing with 91% coverage target
- Test files mirror source structure
- Fixtures load CSV slices for testing

### Data Security
- User data directories (`data/input`, `data/output`, `data/archive`) kept out of git
- Only `data/reference/` (config and NameList.csv) is tracked
- Repository validation prevents accidental data commits

### Code Quality Standards
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking
- **bandit**: Security scanning
- All must pass before commits

## Important Constraints

- Never commit real transaction data to git
- Always maintain encoding fallback chain for Japanese text
- Web UI requires network access - configure WSL2 port forwarding if needed
- Archived files protected from re-processing unless `--force` is used
- Amount-based attendee estimation is configurable via config.toml brackets
- Core members are designated in NameList.csv by setting Core=1

## NameList.csv Schema (v0.4.0+)

```csv
ID,Company,Title,Name,Core
1,Company A,Manager,John Doe,1
2,Company B,Director,Jane Smith,1
3,Company C,Assistant,Bob Jones,0
```

- **Core=1**: Core member (prioritized in random selection)
- **Core=0**: Non-core member (available during editing only)

