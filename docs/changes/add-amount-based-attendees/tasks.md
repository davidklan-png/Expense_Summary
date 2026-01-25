# Implementation Tasks

## 1. Configuration
- [x] 1.1 Add `[processing.amount_based_attendees]` section to config.toml with example brackets
- [x] 1.2 Add `cost_per_person` fallback parameter (default: 3000)
- [x] 1.3 Update Config class to parse amount-based settings

## 2. Core Logic
- [x] 2.1 Update `estimate_attendee_count()` to accept optional amount brackets config
- [x] 2.2 Implement bracket matching logic (find applicable range for amount)
- [x] 2.3 Implement fallback calculation (amount / cost_per_person, min 2)
- [x] 2.4 Add configuration validation with warnings

## 3. Integration
- [x] 3.1 Update CLI to pass amount-based config from Config to selectors
- [x] 3.2 Ensure backward compatibility when config section is missing

## 4. Testing
- [x] 4.1 Add test for bracket-based estimation
- [x] 4.2 Add test for fallback cost-per-person calculation
- [x] 4.3 Add test for backward compatibility (no config section)
- [x] 4.4 Add test for edge cases (boundary values, custom cost-per-person)

## 5. Documentation
- [x] 5.1 Update function docstrings
- [ ] 5.2 Archive change proposal after deployment
