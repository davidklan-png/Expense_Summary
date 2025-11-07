# Decision Log

## Overview
This log captures key architectural and implementation decisions made during the Saison Transform project development, including rationale and trade-offs.

## Decisions

### 2025-11-07: Chardet Library for Encoding Detection

**Decision**: Use chardet library with 0.7 confidence threshold and fallback chain
**Status**: Implemented
**Context**: Phase 2 CSV I/O - need robust handling of mixed Japanese encodings

**Alternatives Considered**:
1. Trial-and-error with multiple encodings
2. Only CP932 (legacy Windows Japanese)
3. Only UTF-8 variants
4. Manual encoding specification via CLI

**Rationale**:
- Japanese CSV files use inconsistent encodings (CP932, UTF-8, UTF-8 BOM)
- Chardet provides statistical confidence scores
- Fallback chain (UTF-8 BOM → UTF-8 → CP932) handles detection failures
- More reliable than pure trial-and-error

**Trade-offs**:
- ✅ Robust handling of real-world data
- ✅ Automatic detection (no user input needed)
- ✅ Statistical confidence scoring
- ❌ External dependency (chardet library)
- ❌ Slight performance overhead

**Impact**: High - affects all CSV input processing

---

### 2025-11-07: Weighted ID Sampling (90/10 Split)

**Decision**: First attendee slot has 90% probability of ID '2', 10% of ID '1'
**Status**: Implemented
**Context**: Phase 2 attendee selection - business requirement for primary contact weighting

**Alternatives Considered**:
1. Pure random sampling (equal probability)
2. Hardcoded ID '2' always first
3. User-configurable probability distribution
4. Amount-based weighting logic

**Rationale**:
- Reflects organizational hierarchy (ID '2' is typical primary contact)
- Randomization provides realistic variance
- Config-driven for easy adjustment
- Tested with statistical verification (1000 trials)

**Trade-offs**:
- ✅ Realistic distribution matching business patterns
- ✅ Configurable via config.toml
- ✅ Statistically validated
- ❌ More complex testing (statistical verification needed)
- ❌ Less predictable than hardcoded approach

**Impact**: Medium - affects attendee selection algorithm

---

### 2025-11-07: Per-File Error Isolation

**Decision**: Continue processing remaining files even if one fails
**Status**: Implemented
**Context**: Phase 2 batch processing - need resilient handling of corrupt/malformed files

**Alternatives Considered**:
1. Fail-fast (abort on first error)
2. Collect errors then fail at end
3. Separate error queue for retry
4. Skip errors silently

**Rationale**:
- Batch processing shouldn't fail entirely due to one corrupt file
- Users can see which files succeeded and which failed
- Enables partial batch completion
- Better UX for large batches

**Trade-offs**:
- ✅ Better user experience
- ✅ Enables partial batch completion
- ✅ Clear error reporting per file
- ❌ Need comprehensive error reporting
- ❌ More complex workflow logic

**Impact**: High - core to production batch processing reliability

---

### 2025-11-07: TDD/BDD Approach with 90% Coverage

**Decision**: Write tests first, achieve ≥90% line coverage
**Status**: Implemented (achieved 91.55%)
**Context**: Phase 2 quality assurance - financial data processing requires high reliability

**Alternatives Considered**:
1. Industry standard 80% coverage
2. 100% coverage requirement
3. Write tests after implementation
4. No formal coverage requirement

**Rationale**:
- Financial data processing requires high reliability
- 90% balances quality with practicality
- Encourages test-first development
- Catches edge cases early
- Safe refactoring with test safety net

**Trade-offs**:
- ✅ Higher code quality and confidence
- ✅ Better edge case coverage
- ✅ Fewer production bugs
- ✅ Safe refactoring
- ❌ Longer initial development time
- ❌ May require creative test design

**Impact**: High - affects all development workflow, achieved 91.55% coverage

---

### 2025-11-07: Poetry with External Virtualenv

**Decision**: Use Poetry's default external virtualenv location instead of in-project
**Status**: Implemented
**Context**: Setting up Python development environment for Phase 1

**Alternatives Considered**:
1. In-project virtualenv with `virtualenvs.in-project = true`
2. Manual venv management
3. Pipenv or pip-tools

**Rationale**:
- External virtualenv is Poetry's default and recommended approach
- Better isolation from project files
- Cleaner git repository (no .venv/ directory)
- Consistent with Poetry best practices

**Trade-offs**:
- ✅ Clean project directory
- ✅ Better IDE integration
- ✅ Standard Poetry workflow
- ❌ Path is user/machine specific
- ❌ Requires Poetry for all developers

**Impact**: Low - development environment only

---

### 2025-11-07: Three-Tier Configuration Precedence

**Decision**: Environment variables > config.toml > pyproject.toml
**Status**: Implemented
**Context**: Configuration system design for flexibility

**Alternatives Considered**:
1. Single config.toml file only
2. Environment variables only
3. Command-line arguments only

**Rationale**:
- Environment variables for deployment overrides
- config.toml for local development settings
- pyproject.toml for package defaults
- Clear precedence order prevents confusion

**Trade-offs**:
- ✅ Flexible for different environments
- ✅ Secure (secrets in env vars)
- ✅ Version-controlled defaults
- ❌ More complex configuration loader
- ❌ Multiple places to check for settings

**Impact**: Medium - affects all configuration handling

---

### 2025-11-07: Relative Path Configuration

**Decision**: Use relative paths from project root in config.toml
**Status**: Implemented
**Context**: Path configuration for Input/Output/Archive directories

**Alternatives Considered**:
1. Absolute paths only
2. Mixed relative/absolute with validation
3. Environment-specific path configs

**Rationale**:
- Portable configuration files
- Works across different machines
- Easy to understand "../Input" pattern
- Resolves to absolute internally

**Trade-offs**:
- ✅ Portable configs
- ✅ Intuitive for developers
- ✅ Version-control friendly
- ❌ Requires careful path resolution
- ❌ May break if project moved

**Impact**: Medium - affects all file I/O operations

---

### 2025-11-07: Per-File Archival Strategy

**Decision**: Archive each file immediately after successful processing
**Status**: Planned for Phase 3
**Context**: Handling partial batch failures gracefully

**Alternatives Considered**:
1. All-or-nothing batch archival
2. End-of-process archival
3. Manual archival step

**Rationale**:
- Resilient to partial failures
- Clear success/failure status per file
- Retry markers for failed files
- No data loss on crash

**Trade-offs**:
- ✅ Granular failure handling
- ✅ Progressive completion
- ✅ Easy retry logic
- ❌ More complex workflow
- ❌ Multiple archive operations

**Impact**: High - core to data pipeline reliability

---

### 2025-11-07: UTF-8 BOM Output Encoding

**Decision**: Always write output files with UTF-8 BOM (utf-8-sig)
**Status**: Implemented
**Context**: Japanese text compatibility requirements

**Alternatives Considered**:
1. Plain UTF-8 without BOM
2. Shift-JIS (cp932) encoding
3. User-configurable encoding

**Rationale**:
- Excel compatibility on Windows
- Preserves Japanese characters
- Industry standard for CSV exchange
- Explicit encoding marker

**Trade-offs**:
- ✅ Excel compatibility
- ✅ Cross-platform support
- ✅ Japanese text preserved
- ❌ 3-byte overhead per file
- ❌ Some tools may not expect BOM

**Impact**: Medium - affects all output files

---

## Decision Template

### YYYY-MM-DD: [Decision Title]

**Decision**: [What was decided]
**Status**: [Proposed|Accepted|Implemented|Deprecated]
**Context**: [Why this decision was needed]

**Alternatives Considered**:
1. [Alternative 1]
2. [Alternative 2]
3. [Alternative 3]

**Rationale**:
- [Key reason 1]
- [Key reason 2]
- [Key reason 3]

**Trade-offs**:
- ✅ [Positive outcome]
- ✅ [Positive outcome]
- ❌ [Negative outcome]
- ❌ [Negative outcome]

**Impact**: [Low|Medium|High] - [Brief impact description]
