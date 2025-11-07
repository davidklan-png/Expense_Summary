# Change Proposal: plan-data-pipeline

## Why
- Phase 2 focuses on the actual ingestion + reporting pipeline described in `docs/spec.txt`.
- After reviewing `docs/spec.txt`, we confirmed the two-phase plan still holds, but Phase 2 must explicitly capture header/encoding detection, attendee-scaling, ID sampling, and duplicate-output handling—this proposal encodes those richer rules.
- We must formalize how files move from Input/Reference through normalized CSVs to HTML, including filename parity and Jinja2 usage.
- Testing expectations (TDD/BDD first, ≥90% coverage) need to be explicitly tied to this phase so implementation cannot skip them.

## What Changes
- Describe the stepwise flow: read Input/Reference, produce processed CSVs, then generate HTML via Jinja2 templates.
- Require that output filenames mirror the source stems for both CSV and HTML artifacts.
- Codify the test-first workflow, covering both unit (TDD) and BDD acceptance tests with the coverage gate.

## Impact
- Provides a spec that developers can implement against without ambiguity when Phase 2 starts.
- Ensures generated artifacts meet compliance/reporting needs (matching filenames, HTML content) while keeping the Phase 1/Phase 2 boundary intact.
- Locks in quality controls early, reducing rework later.
