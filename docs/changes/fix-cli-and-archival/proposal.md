# Fix CLI Architecture and Archival Workflow

## Why

Code review revealed critical deviations from the approved spec:

1. **CLI Architecture**: Hand-parsed `sys.argv` instead of Typer-based CLI with `run`/`validate-config` subcommands
2. **Missing Archival**: No post-processing file movement to `Archive/YYYYMM/`, no retry markers
3. **Missing Month Filtering**: No `--month`, `--force`, or path override support
4. **Data Loss**: Processed CSVs drop non-relevant rows instead of preserving all original data
5. **Ignored Config**: Attendee settings (min/max, weights) from `config.toml` are not used
6. **Security Gaps**: No precedence logging or repo-path validation

These gaps prevent the system from meeting the approved spec requirements in:
- `openspec/changes/archive/2025-11-07-plan-data-pipeline/specs/data-pipeline/spec.md` (CLI Architecture, Month Selection, Archival, Security)
- `openspec/changes/archive/2025-11-07-plan-poetry-environment/specs/environment-setup/spec.md` (validate-config with --dry-run)

## What Changes

### CLI Layer (src/saisonxform/cli.py)
- Replace hand-parsed `sys.argv` with Typer app
- Add `run` subcommand with `--month`, `--force`, `--input`, `--reference`, `--output`, `--archive` options
- Add `validate-config` subcommand with `--dry-run` flag
- Add `sf` alias in pyproject.toml console_scripts
- Log configuration precedence order (CLI > env > config > pyproject)
- Validate paths are not inside git repo

### Month Selection Logic
- Parse `YYYYMM` prefixes from filenames in `Input/`
- Default to latest 2 months if no `--month` specified
- Support explicit month filtering with `--month 202510 --month 202511`
- Check for already-archived months and exit unless `--force`

### Archival Workflow
- Move successfully processed files to `Archive/YYYYMM/`
- Auto-create `Archive/` and month subdirectories
- Create `.retry_YYYYMM.json` on partial failures
- Delete retry marker when all files in month succeed
- Handle cross-filesystem moves and permission errors

### CSV Processing
- Keep ALL rows in processed CSV (not just 会議費/接待費)
- Add attendee columns only for relevant transactions
- Leave attendee columns blank for non-relevant rows

### Configuration Integration
- Read `min_attendees`, `max_attendees` from `config.toml` [processing] section
- Read `primary_id_weights` for weighted ID sampling
- Pass config values to `estimate_attendee_count()` and `sample_attendee_ids()`

**Example config.toml structure**:
```toml
[processing]
min_attendees = 2
max_attendees = 8

# Weighted ID selection for primary slot
# Format: {"id": weight} - weights are normalized to sum to 1.0
primary_id_weights = { "2" = 0.9, "1" = 0.1 }

# Optional: amount-based attendee scaling (future enhancement)
# amount_based_scaling = true
# amount_thresholds = [5000, 10000, 20000]
# attendee_counts = [2, 4, 6, 8]
```

### Tests
- Add CLI invocation tests (Typer subcommands, options)
- Add month filtering tests
- Add archival workflow tests (success, failure, retry markers)
- Add CSV preservation tests (all rows kept)
- Add config integration tests
- Maintain ≥90% coverage

## Impact

### Breaking Changes
- **CLI invocation**: Old `saisonxform process` becomes `saisonxform run` (but `process` can be kept as deprecated alias)
- **Module invocation**: `python -m saisonxform.cli` now requires subcommand: `python -m saisonxform.cli run`

### Migration Path
- Add deprecation warning for bare `saisonxform` or `saisonxform process`
- Suggest `saisonxform run` in warning message
- Keep backward compatibility for 1-2 versions before removal

### Affected Components
- **src/saisonxform/cli.py**: Complete rewrite of CLI layer
- **src/saisonxform/selectors.py**: Add config parameter support
- **tests/test_cli.py**: New CLI invocation tests
- **tests/test_integration.py**: Update to use new CLI
- **pyproject.toml**: Add `sf` alias
- **README.md**: Update all command examples

### Risk Assessment
- **Medium Risk**: Typer dependency adds new requirement (but Poetry already used)
- **Low Risk**: Archival logic isolated, failures leave files in Input/
- **Low Risk**: CSV preservation keeps more data (safe change)
- **Low Risk**: Config integration has sensible defaults

## Dependencies
- Requires Phase 1 (plan-poetry-environment) complete ✅
- Requires Phase 2 (plan-data-pipeline) complete ✅
- Adds new dependency: `typer` (base package) for CLI framework
  - **Rationale**: Required by spec for subcommand architecture
  - **Footprint**: ~30KB, minimal transitive deps (click, typing-extensions)
- Adds new dependency: `rich` for enhanced CLI output
  - **Rationale**: Progress bars, colored output, better UX
  - **Footprint**: ~500KB, no heavy dependencies
  - **Alternative**: Could skip if minimizing dependencies is critical (use plain typer)

## Success Criteria

### Phase 1: CLI Framework ✅ COMPLETE
- [x] `saisonxform run` command implemented with all options
- [x] `sf run` works as alias
- [x] `saisonxform validate-config --dry-run` validates without side effects
- [x] Path overrides (`--input`, `--reference`, `--output`, `--archive`) work
- [x] Configuration precedence logging implemented
- [x] `--verbose` flag for detailed output
- [x] `--version` flag shows version
- [x] `python -m saisonxform.cli` parity maintained
- [x] README updated with new commands
- [x] All existing tests pass (62/62)

### Phase 2-6: Pending Implementation
- [ ] `--month 202510` filters to October 2025 files only
- [ ] `--force` reprocesses already-archived months
- [ ] Processed CSVs contain all original rows
- [ ] Config settings control attendee estimation
- [ ] Archival creates `Archive/YYYYMM/` structure
- [ ] Retry markers created/deleted appropriately
- [ ] Tests for new functionality with ≥90% coverage
