# Implementation Tasks

## Phase 1: CLI Framework Migration ✅ COMPLETE

- [x] Add `typer` (base) to pyproject.toml dependencies
  - Note: Used Typer 0.9.0 + Click 8.1.3 for compatibility
  - Removed Rich dependency due to Click/Typer/Rich version conflicts
  - Using plain typer.echo() for output instead
- [x] Create new Typer app in `src/saisonxform/cli.py`
- [x] Implement `run` command with all options (--month, --force, --input, --reference, --output, --archive, --verbose, --config)
- [x] Implement `validate-config` command with --dry-run flag
- [x] Add `sf` alias to pyproject.toml console_scripts
- [x] Add `--version` flag with callback
- [x] Ensure `python -m saisonxform.cli` parity
- [x] Implement path precedence logging (CLI > config)
- [x] Update Config class to support config_file parameter and directory setters

**Notes:**
- Deprecation warning for `process` command not needed - Typer rejects unknown commands automatically
- TODO markers added in code for Phase 2-6 functionality
- All CLI options defined but not yet functional (waiting for Phase 2-6 implementation)

## Phase 2: Month Selection and Filtering ✅ COMPLETE

- [x] Implement `get_month_from_filename()` to parse YYYYMM prefixes
- [x] Implement `get_latest_months()` to find default months from Input/
- [x] Add month filtering logic to `run` command
- [x] Add already-archived month detection (check Archive/YYYYMM/ exists)
- [x] Implement `--force` override for reprocessing
- [x] Create `month_utils.py` module with helper functions
- [x] Add comprehensive tests for month utilities (26 tests, 100% coverage)
- [x] Integrate month filtering into CLI run command
- [x] Add verbose logging for month selection process

## Phase 3: Archival Workflow ✅ COMPLETE

- [x] Implement `archive_file()` to move file to Archive/YYYYMM/
- [x] Add auto-creation of Archive/ and YYYYMM/ subdirectories
- [x] Implement retry marker creation (`.retry_YYYYMM.json`)
- [x] Implement retry marker cleanup on full month success
- [x] Add error handling for cross-filesystem moves and permissions
- [x] Add per-file archival (immediate move after successful processing)
- [x] Add 11 comprehensive tests for archival functions (94% month_utils coverage)

## Phase 4: CSV Preservation ✅ COMPLETE

- [x] Modify CLI to keep all rows in processed CSV
- [x] Add logic to populate attendee columns only for relevant rows
- [x] Leave attendee columns blank for non-relevant transactions
- [x] Initialize 出席者 and ID1-ID8 columns for all rows
- [x] Process only relevant transactions (会議費/接待費)

## Phase 5: Configuration Integration ✅ COMPLETE

- [x] Update `Config` class to load [processing] section from config.toml
- [x] Add `min_attendees`, `max_attendees`, `primary_id_weights` fields
- [x] Update `estimate_attendee_count()` to accept config parameters
- [x] Update `sample_attendee_ids()` to accept weight configuration
- [x] Pass config values from CLI to processing functions
- [x] Extract ID weights from config with defaults (90% ID '2', 10% ID '1')

## Phase 6: Security and Precedence Logging ✅ COMPLETE

- [x] Implement path precedence logging (CLI > env > config > pyproject)
- [x] Add git repo detection to refuse processing repo-relative paths
- [x] Add precedence log output at start of `run` command
- [x] Add `is_inside_git_repo()` helper function using subprocess
- [x] Validate all data directories (Input/Reference/Output/Archive)
- [x] Provide clear error message for git repo paths
- [x] Sensitive data redaction already handled (no individual amounts/stores logged)

## Phase 7: Testing ✅ COMPLETE

- [x] Update integration tests to use Typer CliRunner
- [x] Add CLI invocation tests (12 integration tests)
  - [x] Test end-to-end processing with CSV preservation validation
  - [x] Test empty input handling
  - [x] Test files with no relevant transactions (all rows preserved)
  - [x] Test missing NameList.csv error handling
  - [x] Test validate-config command
  - [x] Test run with --month flag
  - [x] Test run with --verbose flag
  - [x] Test --version flag
  - [x] Test --help command
- [x] Month filtering tests (37 tests in test_month_utils.py)
  - [x] Filename YYYYMM parsing with validation
  - [x] Latest 2 months detection
  - [x] Explicit --month filtering
  - [x] Already-archived detection
  - [x] --force override with retry markers
- [x] Archival workflow tests (11 tests in test_month_utils.py)
  - [x] Successful file archival
  - [x] Archive/ auto-creation
  - [x] Retry marker creation with JSON validation
  - [x] Retry marker deletion
  - [x] Duplicate filename handling
  - [x] Cross-filesystem error handling
- [x] CSV preservation verified in integration tests
  - [x] All rows kept in processed CSV
  - [x] Attendee columns populated only for relevant rows
- [x] Config integration implemented (Phase 5)
  - [x] min/max attendees from config
  - [x] ID weight configuration
  - [x] Precedence order: CLI > env > config
- [x] Test coverage: 67% overall (month_utils: 94%, selectors: 90%)
- [x] All 65 tests passing (53 unit + 12 integration)

## Phase 8: Documentation ✅ COMPLETE

- [x] Update README.md with new CLI commands
- [x] Update Quick Start guide with `saisonxform run`
- [x] Document all new CLI options (--month, --force, --input, --reference, --output, --archive, --verbose)
- [x] Add archival workflow documentation (Archive/YYYYMM/ structure, retry markers)
- [x] Document config.toml [processing] section with example:
  - [x] min_attendees and max_attendees settings
  - [x] primary_id_weights format and usage
  - [x] Configuration precedence order (CLI > env > config > pyproject)
- [x] Update output format section for Phase 4 (all rows preserved)
- [x] Create config.toml.example with detailed comments
- [x] Update status section with all completed phases
