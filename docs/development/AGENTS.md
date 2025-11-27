<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Repository Guidelines

## Project Structure & Module Organization
- `docs/spec.txt` is the canonical requirements document; keep it updated when behavior shifts.
- `docs/NameList.csv` and `docs/SAISON_2510wtNumbering.csv` are sample datasets—treat them as read-only fixtures.
- Place implementation code under `src/saisonxform/` (create the package before committing) and mirror logical layers (`io.py`, `selectors.py`, `reporting.py`).
- Keep tests in `tests/` with the same module names (`tests/test_selectors.py`) so failures map cleanly to the runtime code.
- Store raw CSV feeds in `data/raw/` (gitignored) and direct outputs to `dist/` to separate reproducible artifacts from inputs.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` – create an isolated Python 3.10+ environment.
- `pip install -r requirements.txt` – install pandas, numpy, chardet, pytest, and any helpers the pipeline uses.
- `python -m saisonxform.pipeline --input data/raw --attendees docs/NameList.csv --output dist` – run the end-to-end transform, emitting processed CSV + HTML.
- `pytest -q` – execute the unit tests; add `-k selector` or `--maxfail=1` to focus on failing areas during investigation.

## Coding Style & Naming Conventions
- Format with `black` (120 columns) and organize imports with `ruff check --fix` or `isort` before committing.
- Prefer fully typed functions, `snake_case` for modules/functions, and `PascalCase` for dataclasses encapsulating attendee metadata.
- Centralize file-system constants in `src/saisonxform/config.py` and expose them through `TypedDict` or `pydantic` models to reduce stringly-typed access.

## Testing Guidelines
- Use `pytest` with fixtures that load lightweight CSV slices from `tests/data/` so selectors stay deterministic.
- Name tests after the behavior under scrutiny (e.g., `test_estimate_attendees_caps_at_eight`).
- Target ≥90% line coverage for the entire `saisonxform` package; add regression tests whenever a bugfix touches parsing, encoding detection, or attendee selection weights.

## Commit & Pull Request Guidelines
- Follow Conventional Commits (`feat: add attendee sampler`, `fix: handle missing headers`) so changelog generation remains trivial.
- Squash WIP commits locally; opened PRs should reference the spec section they modify and list sample commands or screenshots for new outputs.
- Every PR description must include input/output folder paths used during testing plus any new configuration keys introduced.

## Data & Security Notes
- Never commit real transaction CSVs; sanitize sensitive rows before sharing reproductions.
- Validate that `input_folder_path` and `output_folder_path` are configurable through CLI flags or environment variables, and document defaults in `README.md` whenever they change.
