# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Saison Transform is a Python pipeline that processes financial transaction CSV files to identify meeting expenses (會議費) and entertainment expenses (接待費), estimate attendees, assign attendee IDs from a reference list, and generate both processed CSV outputs and HTML reports.

**Core Workflow:**
1. Read transaction CSVs from Input folder with auto-encoding detection
2. Load attendee reference list from NameList.csv
3. Filter transactions by expense category (會議費/接待費 in 備考 column)
4. Estimate attendee count based on transaction amount (利用金額)
5. Sample attendee IDs with weighted selection (90% ID '2', 10% ID '1', plus random sampling)
6. Output processed CSVs + HTML reports to Output folder

## Essential Commands

### Environment Setup
```bash
# Not yet implemented - future Poetry-based setup
# python -m venv .venv && source .venv/bin/activate
# pip install -r requirements.txt

# Once Poetry is implemented (see plan-poetry-environment):
# poetry install
# poetry shell
```

### Running the Pipeline
```bash
# Future command structure (not yet implemented):
# python -m saisonxform.pipeline --input data/raw --attendees docs/NameList.csv --output dist
```

### Testing
```bash
# Future test commands (not yet implemented):
# pytest -q                    # Run all tests
# pytest -k selector           # Run selector tests only
# pytest --maxfail=1           # Stop on first failure
# pytest --cov=saisonxform     # Coverage report (target ≥90%)
```

### Code Quality
```bash
# Future formatting/linting (planned):
# black . --line-length 120
# ruff check --fix
# isort .
```

## OpenSpec Workflow

This project uses OpenSpec for spec-driven development. **Always check OpenSpec before implementing features.**

### Before Any Work
```bash
# Check existing specifications
openspec list --specs         # List all capability specs
openspec list                 # List active change proposals

# View specific items
openspec show <spec-or-change-id>

# Search specifications
rg -n "Requirement:|Scenario:" openspec/specs
```

### Creating Change Proposals

**When to create a proposal:**
- Adding new features or capabilities
- Making breaking changes to APIs or data schemas
- Changing architecture or patterns
- Updating security or performance patterns

**Skip proposals for:**
- Bug fixes that restore spec behavior
- Typos, formatting, comments
- Non-breaking dependency updates

**Proposal workflow:**
1. Review context: Read `openspec/project.md`, run `openspec list` and `openspec list --specs`
2. Choose unique verb-led `change-id` (kebab-case: `add-`, `update-`, `remove-`, `refactor-`)
3. Create directory: `openspec/changes/<change-id>/`
4. Create files:
   - `proposal.md` - Why, what changes, impact
   - `tasks.md` - Implementation checklist with `- [ ]` items
   - `design.md` - Technical decisions (only if cross-cutting, new dependencies, or security/migration complexity)
   - `specs/<capability>/spec.md` - Delta specs with `## ADDED|MODIFIED|REMOVED|RENAMED Requirements`
5. Validate: `openspec validate <change-id> --strict`
6. **Get approval before implementing**

**Implementing changes:**
1. Read `proposal.md`, `design.md` (if exists), and `tasks.md`
2. Implement tasks sequentially
3. Update `tasks.md` checklist: mark each `- [ ]` as `- [x]` after completion
4. Do NOT start until proposal is approved

**After deployment:**
```bash
# Archive completed changes
openspec archive <change-id> --yes

# Validate the archive
openspec validate --strict
```

### Current Active Changes

**plan-poetry-environment** - Establishes Poetry-based environment with:
- Project name: `saisonxform`
- External virtualenvs (default Poetry behavior)
- Minimal deps: `jinja2`, `pytest`
- `templates/` directory for Jinja2 templates
- `config.toml` with paths to Input/Reference/Output folders
- Must complete before Phase 2 work

**plan-data-pipeline** - Implements core pipeline (Phase 2):
- Header/encoding detection
- Transaction filtering by expense category
- Attendee count estimation (2-4 for ≤10K yen, 4-8 for >10K yen)
- Weighted ID sampling (90% ID '2', 10% ID '1')
- CSV + HTML output with filename parity
- TDD/BDD first approach with ≥90% coverage requirement

## Architecture

### Directory Structure
```
.
├── openspec/                  # OpenSpec specifications and proposals
│   ├── project.md            # Project conventions
│   ├── specs/                # Current capability specifications (truth)
│   │   └── <capability>/
│   │       ├── spec.md       # Requirements and scenarios
│   │       └── design.md     # Technical patterns
│   └── changes/              # Proposed changes (not yet implemented)
│       ├── plan-poetry-environment/
│       ├── plan-data-pipeline/
│       └── archive/          # Completed changes
├── docs/                      # Requirements and reference data
│   ├── spec.txt              # Canonical requirements (keep updated)
│   ├── NameList.csv          # Attendee reference list (read-only fixture)
│   └── SAISON_2510wtNumbering.csv  # Sample dataset
├── src/saisonxform/          # Implementation package (to be created)
│   ├── io.py                 # File reading/writing, encoding detection
│   ├── selectors.py          # Attendee estimation and ID sampling
│   ├── reporting.py          # HTML report generation
│   └── config.py             # File-system constants, TypedDict/pydantic models
├── templates/                 # Jinja2 templates for HTML reports (to be created)
├── tests/                     # Mirror src/ structure
│   ├── test_selectors.py     # Unit tests for selection logic
│   └── data/                 # Lightweight CSV fixtures
├── data/                      # External data folders (gitignored)
│   └── raw/                  # Input CSV files
└── dist/                      # Output artifacts (gitignored)
```

### Data Flow
1. **Input**: CSV files in `data/raw/` with columns: 利用日, ご利用店名及び商品名, 利用金額, 備考
2. **Reference**: `docs/NameList.csv` with attendee details (ID, Name, Title, Company)
3. **Processing**:
   - Auto-detect encoding (chardet)
   - Locate header row statically/dynamically
   - Filter transactions where 備考 contains '会議費' or '接待費'
   - Estimate attendees based on 利用金額:
     - Minimum 2 attendees
     - ≤10,000 yen: scale 2-4 attendees
     - >10,000 yen: scale 4-8 attendees
   - Sample attendee IDs:
     - 90% include ID '2'
     - 10% include ID '1'
     - Fill remaining slots with random IDs
     - Sort numerically
4. **Output**:
   - Processed CSV (original + 出席者 + ID1-ID8 columns)
   - HTML report (transaction table + unique attendee list)
   - Files saved to `dist/` with UTF-8 BOM encoding
   - Sequential numbering for duplicate filenames

### Key Technical Requirements
- **Python**: 3.10+
- **Libraries**: pandas, numpy, chardet, jinja2, pytest
- **Encoding**: Auto-detect input, output UTF-8 with BOM (utf-8-sig)
- **ID Handling**: Treat as integers, numeric sorting
- **Error Handling**: Graceful degradation with warnings for missing files, encoding issues, missing columns
- **Testing**: TDD/BDD approach with ≥90% line coverage for entire `saisonxform` package

## Development Workflow

### Code Style
- Format with `black` (120 columns)
- Organize imports with `ruff check --fix` or `isort`
- Fully typed functions (type hints)
- `snake_case` for modules/functions
- `PascalCase` for dataclasses (attendee metadata)
- Centralize constants in `src/saisonxform/config.py`
- Use `TypedDict` or `pydantic` for structured configs

### Testing Guidelines
- Use `pytest` with fixtures loading CSV slices from `tests/data/`
- Name tests after behavior: `test_estimate_attendees_caps_at_eight`
- Target ≥90% line coverage for entire `saisonxform` package
- Add regression tests for bugfixes (parsing, encoding, selection weights)
- Test-first workflow (TDD/BDD)

### Commit Conventions
- Follow Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- Squash WIP commits before PR
- PR description must include:
  - Reference to spec section modified
  - Input/output folder paths used in testing
  - Sample commands or screenshots for new outputs
  - Any new configuration keys introduced

### Data Security
- Never commit real transaction CSVs
- Sanitize sensitive rows before sharing
- Ensure `input_folder_path` and `output_folder_path` are configurable via CLI/env vars
- Document path defaults in README.md

## Key Specifications Reference

**Canonical source**: `docs/spec.txt` - Keep updated when behavior changes

**Required CSV columns (input)**:
- 利用日 (Transaction Date)
- ご利用店名及び商品名 (Store Name and Product Name)
- 利用金額 (Transaction Amount)
- 備考 (Remarks) - Used for filtering '会議費' / '接待費'

**Attendee reference columns**:
- ID (Unique Attendee Identifier)
- Name
- Title
- Company

**Output columns (added)**:
- 出席者 (Estimated attendee count)
- ID1 through ID8 (Selected attendee IDs)

## OpenSpec Best Practices

### Scenario Formatting
**CORRECT** - Use `#### Scenario:` (4 hashtags):
```markdown
#### Scenario: User login success
- **WHEN** valid credentials provided
- **THEN** return JWT token
```

**WRONG**:
```markdown
- **Scenario: User login**      # Don't use bullets
**Scenario**: User login         # Don't use bold text
### Scenario: User login         # Wrong number of hashtags
```

### Delta Operations
- `## ADDED Requirements` - New capabilities (standalone, orthogonal)
- `## MODIFIED Requirements` - Changed behavior (paste full updated requirement)
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes only

**MODIFIED pitfall**: Always paste the complete requirement (header + all scenarios). Partial deltas lose previous details during archiving.

### Validation
```bash
# Always use strict mode
openspec validate <change-id> --strict

# Debug delta parsing
openspec show <change-id> --json --deltas-only

# Check specific requirement
openspec show <spec-id> --json -r 1
```

## Tool Selection Guide

| Task | Tool | Why |
|------|------|-----|
| List specs/changes | openspec CLI | Project structure awareness |
| Find files by pattern | Glob | Fast pattern matching |
| Search code content | Grep | Optimized regex search |
| Read specific files | Read | Direct file access |
| Explore unknown scope | Task agent | Multi-step investigation |
| AST-based code search | ast-grep | Semantic code patterns |

**When to use ast-grep**:
- Searching for code structures (functions, classes, methods)
- Semantic matching (understands syntax, not just text)
- Refactoring patterns across files
- Language-aware searches

**Prefer Grep for**:
- Simple text/regex in any file type
- Non-code files (markdown, JSON, config)
- Known exact text patterns

## Current State

**Status**: Planning phase - no implementation code exists yet
**Active proposals**: plan-poetry-environment (Phase 1), plan-data-pipeline (Phase 2)
**Next steps**: Complete Phase 1 environment setup, then implement Phase 2 pipeline

**Implementation order**:
1. Set up Poetry environment (plan-poetry-environment)
2. Create `src/saisonxform/` package structure
3. Implement pipeline with TDD/BDD approach (plan-data-pipeline)
4. Achieve ≥90% test coverage
5. Archive completed changes with `openspec archive`
