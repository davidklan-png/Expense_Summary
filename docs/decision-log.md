# Decision Log

## Overview
This log captures key architectural and implementation decisions made during the Saison Transform project development, including rationale and trade-offs.

## Decisions

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

### 2025-11-07: 90% Test Coverage Requirement

**Decision**: Enforce ≥90% line coverage for saisonxform package
**Status**: Configured (not yet achieved)
**Context**: Quality assurance standards for Phase 2

**Alternatives Considered**:
1. Industry standard 80% coverage
2. 100% coverage requirement
3. No formal coverage requirement

**Rationale**:
- Financial data processing requires high reliability
- 90% balances quality with practicality
- Encourages TDD/BDD approach
- Catches edge cases early

**Trade-offs**:
- ✅ Higher code quality
- ✅ Better test coverage
- ✅ Fewer production bugs
- ❌ More development time
- ❌ May require test complexity

**Impact**: High - affects all development workflow

---

### 2025-11-07: Per-File Archival Strategy

**Decision**: Archive each file immediately after successful processing
**Status**: Planned for Phase 2
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
**Status**: Configured
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