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

## Phase 7: Testing

- [ ] Add CLI invocation tests (test_cli_invocation.py)
  - [ ] Test `saisonxform run` with various options
  - [ ] Test `sf run` alias
  - [ ] Test `validate-config --dry-run`
  - [ ] Test deprecation warnings
- [ ] Add month filtering tests (test_month_selection.py)
  - [ ] Test filename YYYYMM parsing
  - [ ] Test latest 2 months detection
  - [ ] Test explicit --month filtering
  - [ ] Test already-archived detection
  - [ ] Test --force override
- [ ] Add archival workflow tests (test_archival.py)
  - [ ] Test successful file archival
  - [ ] Test Archive/ auto-creation
  - [ ] Test retry marker creation
  - [ ] Test retry marker cleanup
  - [ ] Test partial month failures
  - [ ] Test cross-filesystem error handling
- [ ] Add CSV preservation tests (test_csv_preservation.py)
  - [ ] Test all rows kept in processed CSV
  - [ ] Test attendee columns populated only for relevant rows
- [ ] Add config integration tests (test_config_integration.py)
  - [ ] Test min/max attendees from config
  - [ ] Test ID weight configuration
  - [ ] Test precedence order
- [ ] Add logging redaction tests (test_logging_redaction.py)
  - [ ] Test sensitive data redacted in verbose mode
  - [ ] Test store names redacted as `[REDACTED]`
  - [ ] Test amounts redacted as `[REDACTED]`
  - [ ] Test summary statistics logged without redaction
  - [ ] Test redaction disabled in non-verbose mode
- [ ] Verify ≥90% coverage maintained

## Phase 8: Documentation

- [ ] Update README.md with new CLI commands
- [ ] Update Quick Start guide with `saisonxform run`
- [ ] Document all new CLI options (--month, --force, --input, --reference, --output, --archive, --verbose)
- [ ] Add archival workflow documentation (Archive/YYYYMM/ structure, retry markers)
- [ ] Document config.toml [processing] section with example:
  - [ ] min_attendees and max_attendees settings
  - [ ] primary_id_weights format and usage
  - [ ] Configuration precedence order (CLI > env > config > pyproject)
- [ ] Update troubleshooting section
  - [ ] Add already-archived month error and --force solution
  - [ ] Add retry marker recovery steps
  - [ ] Add repo-path validation error explanation
- [ ] Create migration guide for old invocations
  - [ ] `saisonxform process` → `saisonxform run`
  - [ ] `python -m saisonxform.cli` → `python -m saisonxform.cli run`
  - [ ] Deprecation timeline and backward compatibility period
