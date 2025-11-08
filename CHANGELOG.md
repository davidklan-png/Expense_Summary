# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2025-11-08

### Added
- **Comprehensive BDD end-to-end tests**: Added 8 BDD-style tests covering complete demo workflow
  - Complete demo workflow with explicit config path
  - Auto-detected config when cd into demo directory
  - Edge cases: missing config with CLI arguments
  - Force reprocessing workflow
  - Demo data quality validation (CSV, NameList, config.toml)
  - Directory structure validation matching documentation
  - Total tests: 144 (136 existing + 8 new), 91% coverage maintained

## [0.2.1] - 2025-11-08

### Fixed
- **Config path resolution for global installations**: Fixed config.toml relative paths when using pipx/pip installations
  - Previously: Relative paths resolved based on package installation directory (e.g., `pipx/venvs/saisonxform/Lib/Reference`)
  - Now: Relative paths correctly resolve based on config.toml file location
  - Enables portable demo directories and proper path resolution with `--config` option
  - Improves user experience for global installations

## [0.2.0] - 2025-11-08

### Added
- **Demo command improvements**: `sf demo` now generates `config.toml` automatically
  - config.toml includes all path configurations
  - Users can simply `cd` into demo directory and run `sf`
  - Better user experience for first-time users
- **CLI simplification**: Removed need for `run` subcommand
  - `sf` now processes files directly (was `sf run`)
  - `run` subcommand still works for backward compatibility
  - Cleaner, more intuitive command structure
- **Global installation support**: Added pipx/pip installation instructions
  - Works as system-wide command without `poetry run`
  - Available on Linux, macOS, Windows WSL
- **Enhanced Makefile**: Added `make ci` for local CI simulation
  - Matches GitHub Actions exactly
  - Prevents push failures by catching issues locally
  - Clear feedback on what will pass/fail in CI

### Changed
- Demo output instructions now show simplified `sf` command
- All documentation updated to use `sf` instead of `sf run`
- README reorganized with better installation options

### Fixed
- Demo command now creates fully functional standalone demo environment
- Config paths are relative to demo directory for portability

## [0.1.0] - 2025-11-07

### Added
- Initial release with core functionality
- Transaction CSV processing with auto-encoding detection
- Attendee estimation and weighted ID assignment
- HTML report generation
- Per-file archival workflow with retry markers
- 91% test coverage with 136 passing tests
- Comprehensive CI/CD with GitHub Actions

[0.2.0]: https://github.com/davidklan-png/Expense_Summary/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/davidklan-png/Expense_Summary/releases/tag/v0.1.0
