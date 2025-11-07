# Quick Start Guide

## 🚀 2-Minute Context

**Project**: Saison Transform - Financial CSV processor for meeting/entertainment expenses
**Language**: Python 3.10+ with Poetry dependency management
**Purpose**: Filter transactions, estimate attendees, generate reports

## Current State (2025-11-07)

### ✅ What's Done
- **Phase 1 Complete**: Poetry environment fully configured
- CLI skeleton with `validate-config` command
- Configuration system (env vars > config.toml > pyproject.toml)
- HTML report template (Japanese)
- Package structure at `src/saisonxform/`

### 🚧 What's Next
- **Phase 2 Starting**: Data pipeline implementation (0/6 tasks)
- Need to implement CSV I/O, attendee selection, report generation
- Target ≥90% test coverage with TDD approach

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

# 5. Check OpenSpec status
openspec list
openspec show plan-data-pipeline
```

## Key Files to Know

### Configuration
- `config.toml` - Application settings
- `pyproject.toml` - Poetry/package config
- `.env` - Environment overrides (optional)

### Source Code
- `src/saisonxform/config.py` - Configuration loader (173 lines)
- `src/saisonxform/cli.py` - CLI entry point (65 lines)
- `src/saisonxform/io.py` - **TODO**: CSV I/O (Phase 2)
- `src/saisonxform/selectors.py` - **TODO**: Attendee logic (Phase 2)

### Templates
- `templates/report.html.j2` - HTML report template

### Specifications
- `openspec/changes/plan-data-pipeline/` - Phase 2 specs
- `docs/spec.txt` - Original requirements

## Essential Commands

```bash
# Development
poetry run saisonxform validate-config  # Check configuration
poetry run pytest                       # Run tests (none yet)
poetry run black .                      # Format code
poetry run ruff check                   # Lint code

# OpenSpec
openspec validate plan-data-pipeline --strict  # Validate proposal
openspec archive plan-poetry-environment --yes # Archive completed

# Git
git status                              # Check changes
git diff                               # Review modifications
```

## Data Flow Overview

```
Input/ → Filter (会議費/接待費) → Estimate (2-8 attendees) → Sample IDs → Output/ + Archive/
```

1. **Input**: CSV files with Japanese transaction data
2. **Filter**: Select only meeting/entertainment expenses
3. **Estimate**: Random 2-8 attendees per transaction
4. **Sample**: 90% ID '2', 10% ID '1', rest random
5. **Output**: Enhanced CSV + HTML report
6. **Archive**: Move processed files by month

## Project Conventions

- **TDD First**: Write tests before implementation
- **OpenSpec**: Check specs before coding
- **Coverage**: Maintain ≥90% line coverage
- **Encoding**: UTF-8 BOM for outputs
- **Paths**: Relative from project root
- **IDs**: Treat as integers, sort numerically

## Common Tasks

### Continue Phase 2 Development
```bash
cd /Users/frank/Projects/saisonxform
poetry shell
openspec show plan-data-pipeline
# Start with tests/test_io.py
```

### Run Pipeline (Future)
```bash
poetry run saisonxform process --month 202510
poetry run saisonxform process --input ../Input --output ../Output
```

### Check Test Coverage (Future)
```bash
poetry run pytest --cov=saisonxform --cov-report=html
open htmlcov/index.html
```

## Need Help?

1. Check `docs/spec.txt` for requirements
2. Review `openspec/changes/` for implementation plans
3. See `README.md` for detailed documentation
4. Check `docs/sessions/` for previous work context

## Current Focus

**Immediate Priority**: Start Phase 2 TDD implementation
1. Create `tests/test_io.py` with encoding detection tests
2. Implement `src/saisonxform/io.py` to pass tests
3. Continue with selectors, reporting modules
4. Achieve ≥90% coverage before moving on