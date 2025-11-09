# Quick Start Guide

## 🚀 2-Minute Context

**Project**: Saison Transform - Financial CSV processor for meeting/entertainment expenses
**Language**: Python 3.10+ with Poetry dependency management
**Purpose**: Filter transactions, estimate attendees, generate reports

## Current State (2025-11-07)

### ✅ What's Done
- **Phase 1 Complete**: Poetry environment fully configured
- **Phase 2 Complete**: Full data pipeline with 91.55% test coverage
- CLI with `validate-config` and `process` commands
- CSV I/O with encoding detection (chardet + fallback chain)
- Attendee selection with weighted ID sampling (90/10)
- HTML report generation with Jinja2 templates
- 62 comprehensive tests, all passing

### 🚧 What's Next
- **Phase 3 Planning**: Archival workflow with retry markers
- Per-file archival to Archive/YYYYMM/
- Already-processed month detection with --force override
- Retry marker creation/cleanup

## Get Started in 30 Seconds

```bash
# 1. Navigate to project
cd /Users/frank/Projects/saisonxform

# 2. Install dependencies
poetry install

# 3. Activate environment
poetry shell

# 4. Verify setup
poetry run saisonxform validate-config

# 5. Process CSV files
poetry run saisonxform process
```

## Key Files to Know

### Configuration
- `config.toml` - Application settings (paths, estimator bounds)
- `pyproject.toml` - Poetry/package config
- `.env` - Environment overrides (optional)

### Source Code (Implemented)
- `src/saisonxform/config.py` - Configuration loader
- `src/saisonxform/cli.py` - CLI with validate-config + process commands
- `src/saisonxform/io.py` - CSV I/O with encoding detection
- `src/saisonxform/selectors.py` - Transaction filtering + attendee selection
- `src/saisonxform/reporting.py` - HTML report generation

### Templates
- `templates/report.html.j2` - HTML report template (Japanese)

### Tests (62 tests, 91.55% coverage)
- `tests/test_io.py` - CSV I/O tests (11 tests)
- `tests/test_selectors.py` - Attendee logic tests (16 tests)
- `tests/test_reporting.py` - HTML generation tests (13 tests)
- `tests/test_integration.py` - End-to-end pipeline tests (11 tests)
- `tests/test_edge_cases.py` - Error handling tests (11 tests)
- `tests/data/` - Test fixtures (sample CSV, namelist)

### Specifications
- `docs/spec.txt` - Original requirements
- `openspec/archive/plan-poetry-environment/` - Phase 1 (archived)
- `openspec/archive/plan-data-pipeline/` - Phase 2 (archived)

## Essential Commands

```bash
# Development
poetry run saisonxform validate-config  # Check configuration
poetry run saisonxform process          # Run pipeline
poetry run pytest -q                    # Run all tests
poetry run pytest --cov=saisonxform     # Test with coverage
poetry run black .                      # Format code
poetry run ruff check                   # Lint code

# Testing
poetry run pytest -k test_io            # Run specific test file
poetry run pytest --maxfail=1           # Stop on first failure
poetry run pytest -v                    # Verbose output

# OpenSpec
openspec list                           # List change proposals
openspec list --specs                   # List capability specs
openspec validate <change-id> --strict  # Validate proposal
openspec archive <change-id> --yes      # Archive completed change

# Git
git status                              # Check changes
git diff                                # Review modifications
```

## Data Flow Overview

```
Input/ → Encoding Detection → Filter (会議費/接待費) →
Estimate (2-8) → Sample IDs (90/10) → CSV + HTML → Output/
```

1. **Input**: CSV files with Japanese transaction data
2. **Encoding**: Auto-detect (UTF-8 BOM → UTF-8 → CP932)
3. **Filter**: Select only meeting/entertainment expenses (備考 column)
4. **Estimate**: Random 2-8 attendees per transaction
5. **Sample**: 90% ID '2', 10% ID '1', rest random from reference
6. **Output**: Enhanced CSV (UTF-8 BOM) + HTML report
7. **Archive**: (Phase 3) Move processed files by month

## Project Conventions

- **TDD First**: Write tests before implementation
- **OpenSpec**: Check specs before coding
- **Coverage**: Maintain ≥90% line coverage (current: 91.55%)
- **Encoding**: UTF-8 BOM for outputs, auto-detect for inputs
- **Paths**: Relative from project root
- **IDs**: Treat as integers, sort numerically

## Common Tasks

### Run the Pipeline

```bash
cd /Users/frank/Projects/saisonxform
poetry shell

# Basic usage (uses config.toml paths)
poetry run saisonxform process

# Custom paths
poetry run saisonxform process \
  --input /path/to/Input \
  --reference /path/to/Reference \
  --output /path/to/Output
```

### Check Test Coverage

```bash
poetry run pytest --cov=saisonxform --cov-report=html
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Single test file
poetry run pytest tests/test_selectors.py -v

# Single test function
poetry run pytest tests/test_selectors.py::test_weighted_id_selection -v

# All integration tests
poetry run pytest tests/test_integration.py -v
```

### Format and Lint Code

```bash
# Format with Black
poetry run black . --line-length 120

# Check formatting without changes
poetry run black . --check

# Lint with Ruff
poetry run ruff check --fix
```

## Need Help?

1. Check `README.md` for comprehensive documentation
2. Review `docs/spec.txt` for original requirements
3. See `docs/sessions/` for development history
4. Check `openspec/archive/` for completed change proposals
5. Review test files for usage examples

## Current Focus

**Immediate Priority**: Plan Phase 3 archival workflow
1. Create OpenSpec change proposal for archival features
2. Implement per-file archival to Archive/YYYYMM/
3. Add retry marker creation/cleanup
4. Add already-processed month detection with --force flag
5. Write comprehensive tests for archival logic

## Troubleshooting

**Tests fail with import errors:**
```bash
poetry install  # Reinstall dependencies
poetry shell    # Ensure virtualenv is active
```

**Encoding errors when processing CSV:**
- Check file encoding with: `file -I your_file.csv`
- Pipeline tries UTF-8 BOM → UTF-8 → CP932 automatically
- Add more fallbacks in `io.py` if needed

**Coverage below 90%:**
- Run: `poetry run pytest --cov=saisonxform --cov-report=term-missing`
- Focus on untested branches (see "Missing" column)
- Add edge case tests for uncovered lines
