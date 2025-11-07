# Change Proposal: plan-poetry-environment

## Why
- Phase 1 requires a clearly documented Poetry-managed setup before we touch business logic.
- Contributors need guidance on project naming (`saisonxform`), where virtualenvs live, and how template files fit into the repo.
- External Input/Reference/Output folders must be documented with `config.toml`-driven relative paths so all future work shares the same contract.

## What Changes
- Define the environment baseline using Poetry with minimal deps (`jinja2`, `pytest`) and default external virtualenvs.
- Specify the presence/location of the `templates/` directory for Jinja2.
- Capture the requirements for `config.toml` and the three sibling data folders, including how paths resolve.

## Impact
- Establishes the tooling and configuration prerequisites for Phase 2.
- Prevents ad-hoc virtualenv or folder layouts that could break automation or onboarding.
- Gives reviewers a concrete spec to validate before accepting any environment-related PRs.
