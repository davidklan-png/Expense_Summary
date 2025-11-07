# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - 2025-11-07
- Poetry-based Python project structure with pyproject.toml
- Three-tier configuration system (env vars > config.toml > pyproject.toml)
- CLI skeleton with `validate-config` command
- Configuration loader with path resolution and validation
- Jinja2 HTML report template with Japanese support
- Comprehensive project documentation in README.md
- Session documentation system in docs/
- Test structure with data fixtures directory
- OpenSpec compliance for plan-poetry-environment

### Project Setup
- Python 3.10+ support with Poetry dependency management
- Dependencies: pandas, numpy, chardet, jinja2 for data processing
- Dev dependencies: pytest, pytest-cov, black, ruff, isort
- External virtualenv configuration (Poetry default)
- 90% test coverage target configured

### Documentation
- Quick Start guide for 2-minute onboarding
- Project Status dashboard
- Decision Log with architectural choices
- Session Index for development history

## [0.1.0] - TBD

Initial release (planned after Phase 2 completion)