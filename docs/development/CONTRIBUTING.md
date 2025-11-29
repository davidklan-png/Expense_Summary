# Contributing to Saison Transform

Thank you for your interest in contributing to Saison Transform! This guide will help you get started with development.

## Development Setup

### Prerequisites

- Python 3.10 - 3.13
- Poetry (dependency management)
- Git

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd saisonxform

# Install dependencies
poetry install

# Install pre-commit hooks
make pre-commit-install
# OR: poetry run pre-commit install
```

## Code Quality Standards

This project enforces strict code quality standards through automated checks:

### Formatting

- **Black**: Code formatting (120 char line length)
- **isort**: Import sorting (black profile)

```bash
# Auto-format code
make format

# OR manually:
poetry run black .
poetry run isort .
```

### Linting

- **Ruff**: Fast Python linter (replaces flake8, pylint, etc.)
  - Checks: pycodestyle, pyflakes, isort, comprehensions, bugbear, pyupgrade, naming, security, builtins, commas, print statements

```bash
# Run linter
make lint

# Auto-fix issues
make lint-fix

# OR manually:
poetry run ruff check .
poetry run ruff check --fix .
```

### Type Checking

- **mypy**: Static type checking

```bash
# Run type checker
make type-check

# OR manually:
poetry run mypy src/saisonxform
```

### Security Scanning

- **bandit**: Security vulnerability scanner

```bash
# Run security scan
make security

# OR manually:
poetry run bandit -r src/saisonxform -ll
```

### Running All Checks

```bash
# Run all quality checks (format + lint + type + security + test)
make qa

# Simulate CI checks locally
make ci
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
poetry run pytest tests/test_io.py

# Run tests matching a pattern
poetry run pytest -k "test_filter"
```

### Test Coverage Requirements

- **Minimum coverage**: 90% (currently 54% - Phase 1 CLI code not yet tested)
- Coverage is automatically checked in CI
- View HTML coverage report: `open htmlcov/index.html`

### Writing Tests

- Follow TDD/BDD approach (write tests first)
- Place tests in `tests/` directory, mirroring `src/` structure
- Name tests descriptively: `test_<behavior>_<expected_outcome>`
- Use fixtures for common setup (see `tests/conftest.py`)

## Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system or dependency changes
- `chore`: Other changes that don't modify src or test files

### Examples

```bash
feat(cli): add month filtering with --month option

Implements Phase 2 month selection logic with YYYYMM filename parsing.
Supports multiple --month flags for processing specific months.

Closes #42
```

```bash
fix(io): handle UTF-8 BOM encoding detection

CSV files with UTF-8 BOM were not being detected correctly.
Added utf-8-sig to encoding fallback chain.
```

### Using Commitizen

```bash
# Interactive commit message creator
poetry run cz commit

# Check commit message format
poetry run cz check --commit-msg-file .git/COMMIT_EDITMSG
```

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality:

### Installed Hooks

1. **Black** - Code formatting
2. **isort** - Import sorting
3. **Ruff** - Linting (with auto-fix)
4. **mypy** - Type checking (excluding tests)
5. **bandit** - Security scanning
6. **General checks** - Trailing whitespace, YAML/TOML syntax, large files, merge conflicts, private keys
7. **Commitizen** - Commit message validation

### Running Hooks Manually

```bash
# Run all hooks on staged files
poetry run pre-commit run

# Run all hooks on all files
make pre-commit-run
# OR: poetry run pre-commit run --all-files

# Run specific hook
poetry run pre-commit run black --all-files
```

### Skipping Hooks (Not Recommended)

```bash
# Skip pre-commit hooks (use only when necessary)
git commit --no-verify -m "your message"
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b add-new-feature develop
```

### 2. Make Changes

Follow the code style and testing guidelines above.

### 3. Run Quality Checks

```bash
# Format code
make format

# Run all checks
make qa

# OR run CI simulation
make ci
```

### 4. Commit Changes

```bash
# Add files
git add .

# Commit (pre-commit hooks run automatically)
git commit

# OR use commitizen for guided commit
poetry run cz commit
```

### 5. Push and Create Pull Request

```bash
git push origin add-new-feature
```

Then create a pull request on GitHub targeting `develop` branch.

## Pull Request Requirements

### Before Submitting

- [ ] All tests pass: `make test`
- [ ] Code is formatted: `make format`
- [ ] Linting passes: `make lint`
- [ ] Type checking passes: `make type-check` (warnings OK for now)
- [ ] Security scan clean: `make security` (warnings OK for now)
- [ ] Test coverage ≥90% (or equivalent to current level)
- [ ] Commit messages follow conventional commits
- [ ] Documentation updated (README.md, docstrings, CONTRIBUTING.md if needed)

### PR Description Should Include

- **What**: Summary of changes
- **Why**: Motivation and context
- **How**: Implementation approach
- **Testing**: How changes were tested
- **Screenshots**: If applicable (for UI changes)
- **Related Issues**: Closes #123, Relates to #456

## OpenSpec Workflow

This project uses OpenSpec for specification-driven development.

### Before Adding Features

```bash
# Check existing specifications
openspec list --specs
openspec list

# View specific spec
openspec show <spec-or-change-id>
```

### Creating Change Proposals

For major changes (new features, breaking changes, architecture changes):

1. Create proposal: `openspec/changes/<change-id>/proposal.md`
2. Create tasks: `openspec/changes/<change-id>/tasks.md`
3. Create delta specs: `openspec/changes/<change-id>/specs/<capability>/spec.md`
4. Validate: `openspec validate <change-id> --strict`
5. Get approval before implementing

See `CLAUDE.md` for detailed OpenSpec workflow.

## Code Style Guidelines

### Python Style

- **Line length**: 120 characters (enforced by black)
- **Imports**: Sorted with isort (black profile)
- **Type hints**: Required for all functions (checked by mypy)
- **Docstrings**: Google style for public functions
- **Naming**:
  - `snake_case` for functions, variables, modules
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Example

```python
"""Module for processing CSV files."""
from pathlib import Path
from typing import List, Optional

import pandas as pd


def read_csv_with_detection(file_path: Path) -> tuple[pd.DataFrame, str]:
    """Read CSV file with automatic encoding detection.

    Args:
        file_path: Path to the CSV file

    Returns:
        Tuple of (DataFrame, detected_encoding)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If CSV cannot be parsed
    """
    # Implementation here
    pass
```

## CI/CD Pipeline

GitHub Actions runs on all pushes and pull requests:

### Jobs

1. **Lint** (Python 3.10)
   - Black formatting check
   - isort import order check
   - Ruff linting

2. **Test** (Python 3.10, 3.11, 3.12, 3.13)
   - Run pytest with coverage
   - Upload coverage to Codecov

3. **Type Check** (Python 3.10)
   - mypy static type checking
   - Currently non-blocking (continue-on-error)

4. **Security** (Python 3.10)
   - bandit security scanning
   - Currently non-blocking (continue-on-error)

### CI Badge Status

Add to README.md:

```markdown
![CI](https://github.com/your-org/saisonxform/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/your-org/saisonxform/branch/develop/graph/badge.svg)](https://codecov.io/gh/your-org/saisonxform)
```

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: See `docs/` directory and `openspec/` specifications
- **Questions**: Create a GitHub Discussion or open an issue

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
