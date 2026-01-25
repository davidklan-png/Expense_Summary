# Change: Add Amount-Based Attendee Estimation

## Why
Currently, attendee estimation uses pure random distribution between min/max bounds regardless of transaction amount. This doesn't reflect reality - higher transaction amounts typically indicate more attendees. We need configurable amount-based estimation with sensible fallback behavior.

## What Changes
- Add `[processing.amount_based_attendees]` section to config.toml
- Support amount brackets mapping to attendee count ranges with random selection
- Fallback to cost-per-person calculation (¥3,000/person, min 2) when no brackets match
- Validate configuration at startup with warnings (non-fatal)
- Maintain backward compatibility - if section is missing, use current random behavior

## Impact
- Affected specs: data-pipeline (Attendee Estimation Logic requirement)
- Affected code:
  - `src/saisonxform/config.py` - Load amount-based settings
  - `src/saisonxform/selectors.py` - Implement amount-based estimation
  - `src/saisonxform/cli.py` - Pass config to selectors
  - `config.toml` - Add new configuration section
- **BREAKING**: None - fully backward compatible
