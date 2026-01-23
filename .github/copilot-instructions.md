# Copilot Instructions for Saison Transform

This document provides essential guidelines for AI coding agents working on the Saison Transform project. Follow these instructions to ensure consistency and alignment with the project's architecture, workflows, and conventions.

## Project Overview
Saison Transform is a Python-based pipeline for processing financial transaction CSV files. The primary goals of the project include:
- Identifying meeting expenses () and entertainment expenses ().
- Estimating attendees and assigning IDs from a reference list.
- Generating processed CSV outputs and HTML reports.

### Core Workflow
1. Read transaction CSVs from the input folder with auto-encoding detection.
2. Load attendee reference list from `docs/NameList.csv`.
3. Filter transactions by expense category (/ in the 	 column).
4. Estimate attendee count based on transaction amount.
5. Sample attendee IDs with weighted selection (90% ID '2', 10% ID '1', plus random sampling).
6. Output processed CSVs and HTML reports to the output folder.

## Repository Structure
- **`src/saisonxform/`**: Core implementation of the pipeline. Organize code by logical layers (e.g., `io.py`, `selectors.py`, `reporting.py`).
- **`tests/`**: Unit tests for the project. Follow the same module naming convention (e.g., `tests/test_selectors.py`).
- **`data/`**: Contains raw input data and reference files. Raw CSV feeds are stored in `data/raw/` (gitignored), and outputs are directed to `dist/`.
- **`docs/`**: Documentation, including `spec.txt` (canonical requirements document) and sample datasets like `NameList.csv`.
- **`examples/`**: Example implementations and demos, including React components and UI showcases.

## Development Workflows

### Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline
Run the end-to-end transformation pipeline:
```bash
python -m saisonxform.pipeline --input data/raw --attendees docs/NameList.csv --output dist
```

### Testing
Run unit tests with:
```bash
pytest -q
```
- Use `-k <test_name>` to run specific tests.
- Add `--maxfail=1` to stop after the first failure.

### Linting and Formatting
- Format code with `black` (120 columns):
  ```bash
  black .
  ```
- Organize imports with `ruff check --fix` or `isort`:
  ```bash
  ruff check --fix
  ```

## Key Conventions
- Use `snake_case` for functions and variables.
- Use `PascalCase` for dataclasses (e.g., attendee metadata).
- Centralize file-system constants in `src/saisonxform/config.py` and expose them through `TypedDict` or `pydantic` models.
- Follow the spec-driven development process outlined in `openspec/AGENTS.md`.

## Spec-Driven Development
This project uses OpenSpec for managing changes and specifications. Refer to `openspec/AGENTS.md` for detailed instructions on:
- Creating and applying change proposals.
- Writing and validating specs.
- Following the three-stage workflow for changes.

## External Dependencies
- Python 3.10+ is required.
- Key libraries include `pandas`, `numpy`, `chardet`, and `pytest`.
- React components for UI examples are located in `examples/`.

## Additional Resources
- [README.md](../README.md): Main project documentation.
- [docs/spec.txt](../docs/spec.txt): Canonical requirements document.
- [docs/NameList.csv](../docs/NameList.csv): Sample attendee reference list.
- [openspec/AGENTS.md](../openspec/AGENTS.md): Spec-driven development guidelines.
- [tests/ui_tests/README.md](../tests/ui_tests/README.md): UI testing documentation.

For further assistance, consult the project maintainers or refer to the documentation in the `docs/` folder.