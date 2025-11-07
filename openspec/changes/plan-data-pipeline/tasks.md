# Tasks
- [x] Phase2-1: Re-read `docs/spec.txt` to extract the ingestion, attendee estimation, and reporting rules.
- [x] Phase2-2: Specify the CSV normalization flow and filename requirements.
- [x] Phase2-3: Describe Jinja2-driven HTML output expectations that pair with the processed CSVs.
- [x] Phase2-4: Capture the TDD + BDD workflow plus ≥90% coverage mandate in the spec.
- [x] Phase2-5: Validate the planning artifacts with `openspec validate plan-data-pipeline --strict` (still pre-implementation) and resolve issues. DoD evidence: capture the validation summary in `evidence.md`.
- [x] Phase2-6: Populate `evidence.md` with links to specs, diffs, and test logs demonstrating completion of Phase 2 tasks.

## Implementation Tasks (Completed)
- [x] Implement CSV I/O module (`src/saisonxform/io.py`) with encoding detection and header parsing
- [x] Implement attendee selectors (`src/saisonxform/selectors.py`) with filtering and weighted ID sampling
- [x] Implement HTML reporting (`src/saisonxform/reporting.py`) with Jinja2 template rendering
- [x] Update CLI (`src/saisonxform/cli.py`) with `process` command
- [x] Write comprehensive unit tests for all modules
- [x] Write integration tests for end-to-end pipeline
- [x] Achieve ≥90% test coverage (achieved: 91.55%)
- [x] Update template (`templates/report.html.j2`) to match context structure
