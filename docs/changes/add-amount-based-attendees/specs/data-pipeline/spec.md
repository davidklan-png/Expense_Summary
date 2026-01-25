# data-pipeline Delta Specification

## MODIFIED Requirements

### Requirement: Attendee Estimation Logic
Attendee counts and ID selection MUST follow the ranges and probability weighting defined in `config.toml`, supporting both amount-based bracket estimation and pure random sampling within bounds.

#### Scenario: Amount-based bracket estimation
- **WHEN** a transaction is processed AND `[processing.amount_based_attendees]` brackets are defined in config
- **THEN** the system finds the matching bracket for the transaction amount, randomly selects an attendee count between the bracket's min and max values, and uses that count for attendee assignment.

#### Scenario: Fallback cost-per-person calculation
- **WHEN** a transaction amount doesn't match any configured bracket
- **THEN** the system calculates attendees as `max(2, amount / cost_per_person)` where `cost_per_person` defaults to 3000 yen, ensuring a minimum of 2 attendees.

#### Scenario: Backward compatibility without amount config
- **WHEN** no `[processing.amount_based_attendees]` section exists in config
- **THEN** the system uses uniform random distribution between `min_attendees` (default 2) and `max_attendees` (default 8) as before.

#### Scenario: Invalid bracket configuration
- **WHEN** amount brackets have gaps, overlaps, or invalid values
- **THEN** the system logs a warning at startup, disables amount-based estimation for that session, and falls back to uniform random distribution.

#### Scenario: Randomized scaling (existing behavior)
- **WHEN** a transaction categorized as `会議費` or `接待費` is processed AND amount-based estimation is disabled
- **THEN** the estimated attendee count is drawn randomly between the configured `min_attendees` (default 2) and `max_attendees` (default 8).

#### Scenario: ID sampling
- **WHEN** attendee IDs are assigned per transaction
- **THEN** the pipeline uses weighted random selection: ID `2` has weight 0.9, ID `1` has weight 0.1 for the primary slot, remaining slots are filled by sampling without replacement from the reference list according to weights defined in `config.toml`, and the final list is padded with blanks up to `ID8` before sorting numerically.
