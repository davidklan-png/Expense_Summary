# UI Improvement and Core Attendee Feature Implementation

## Overview

You are tasked with evaluating and improving the Streamlit-based web UI for the Saison Transform expense processing application. The goals are:

1. **UI Simplification** - Make the interface more elegant, intuitive, and easier to use
2. **Core Attendee Feature** - Implement a core member system where designated attendees are prioritized in random selection

---

## Part 1: UI Evaluation and Improvement

### Current State Analysis

The current UI (`web_app.py`) uses a 3-step workflow:
1. **Upload** - File upload via drag-and-drop
2. **Process & Edit** - Auto-processing with data editor
3. **Download** - Export to CSV/Excel/HTML/ZIP

**Components to Review:**
- `web_app.py` - Main application entry point
- `src/saisonxform/web/` - UI modules:
  - `sticky_header.py` - Fixed header with step indicator
  - `step_upload.py` - File upload step
  - `step_process.py` - Processing and editing step
  - `step_download.py` - Download/export step
  - `workflow_styles.py` - CSS styling
  - `workflow_state.py` - State management
  - `translations.py` - i18n support (EN/JA)

### UI Improvement Requirements

#### 1. Visual Design
- Reduce visual clutter and unnecessary UI elements
- Use consistent spacing, typography, and color scheme
- Ensure clear visual hierarchy between steps
- Remove redundant status indicators or badges
- Consider a cleaner, more modern aesthetic

#### 2. Workflow Simplification
- Evaluate if 3 steps are necessary or if workflow can be condensed
- Remove friction points in the user journey
- Make step transitions more intuitive
- Consider auto-advancing when logical (e.g., after upload completes)

#### 3. Editor Experience
- Simplify the data editor interface
- Make attendee editing more intuitive
- Consider inline editing improvements
- Ensure the 人数 (attendee count) column updates correctly when IDs change

#### 4. Sidebar Optimization
- Evaluate sidebar necessity and content
- Consider moving configuration to a settings modal or collapsible section
- Attendee reference list should be easily accessible but not dominating

#### 5. Responsive Design
- Ensure proper behavior on different screen sizes
- Test sticky header behavior
- Verify scroll behavior and step navigation

#### 6. Accessibility
- Clear labels and instructions
- Proper contrast ratios
- Keyboard navigation support

### Deliverables for UI Improvement

1. Document current pain points with specific examples
2. Propose UI changes with mockups or detailed descriptions
3. Implement approved changes
4. Update related CSS in `workflow_styles.py`
5. Ensure all translations are updated in `translations.py`

---

## Part 2: Core Attendee Feature Implementation

### Feature Description

Implement a **Core Member** system for attendee assignment:
- **Core Members**: Designated key attendees who should be included first
- **Non-Core Members**: Additional attendees available for selection during editing

### NameList.csv Schema Update

**Current Schema:**
```csv
ID,Company,Title,Name
```

**New Schema:**
```csv
ID,Company,Title,Name,Core
```

**Core Column Values:**
- `1` = Core member (prioritized in random selection)
- `0` = Non-core member (available during editing only)

### Implementation Requirements

#### 1. Update `selectors.py`

**Current `sample_attendee_ids()` behavior:**
- Uses weighted selection (90% ID "2", 10% ID "1")
- Fills remaining slots with random sample from all IDs

**New behavior:**
1. Load Core members from NameList.csv where `Core=1`
2. Randomly select from Core members first to fill initial slots
3. Pad remaining slots for manual editing (show non-core members in editor)
4. Remove hardcoded ID weights ("1" and "2") - use Core column instead

**Function signature update:**
```python
def sample_attendee_ids(
    count: int,
    available_ids: list[str],
    core_ids: list[str],       # NEW: List of core member IDs
    return_dict: bool = False
) -> list[str] | dict[str, str]:
```

**Algorithm:**
1. Shuffle core_ids randomly
2. Take up to `count` IDs from shuffled core_ids
3. If count > len(core_ids), fill remaining from non-core (or leave empty for editing)
4. Sort numerically and pad to 8 slots

#### 2. Update `web_app.py`

- Load Core column when reading NameList.csv
- Pass core_ids to `sample_attendee_ids()`
- Update editor to show core vs non-core distinction
- Consider visual indicator (e.g., star icon) for core members in dropdown

#### 3. Update `config.py` and `config.toml`

- Remove `primary_id_weights` configuration (replaced by Core column)
- Add optional `core_fill_strategy` setting:
  - `"random"` (default) - Randomly select from core members
  - `"sequential"` - Use core members in ID order

**Updated config.toml:**
```toml
[processing]
min_attendees = 2
max_attendees = 8
core_fill_strategy = "random"  # or "sequential"

# REMOVE these lines:
# [processing.primary_id_weights]
# "2" = 0.9
# "1" = 0.1
```

#### 4. Update Editor UI

When editing attendees in Step 2:
- Dropdown should show all members (core and non-core)
- Core members should be visually distinguished (bold, icon, or grouped)
- Consider grouping: "Core Members" section at top, "Other Members" below

#### 5. Update HTML Report Template

- Consider adding Core indicator in attendee details section
- Optional: Show core members with subtle visual distinction

#### 6. Update Tests

Update test files to cover:
- `test_selectors.py`:
  - Test core_ids parameter handling
  - Test random selection from core members
  - Test fallback when not enough core members
  - Test backward compatibility if core_ids not provided

- Integration tests:
  - Test full workflow with Core column in NameList.csv
  - Test editor behavior with core/non-core distinction

### Migration Considerations

1. **Backward Compatibility**: Handle NameList.csv files without Core column
   - Default all members to Core=0 if column missing
   - Log warning about missing Core column

2. **Validation**:
   - Warn if no Core members defined
   - Ensure at least 2 core members for typical workflows

---

## Part 3: Implementation Checklist

### UI Improvements
- [ ] Audit current UI and document issues
- [ ] Design simplified workflow (propose changes)
- [ ] Update `workflow_styles.py` with cleaner CSS
- [ ] Simplify sticky header design
- [ ] Improve editor UX
- [ ] Update translations for any new text
- [ ] Test responsive behavior
- [ ] Update any affected documentation

### Core Attendee Feature
- [ ] Update NameList.csv with Core column
- [ ] Update `selectors.py` with new algorithm
- [ ] Update `config.py` to remove ID weights, add core_fill_strategy
- [ ] Update `config.toml` reference file
- [ ] Update `web_app.py` to use core member logic
- [ ] Update editor to show core/non-core distinction
- [ ] Update HTML report template (optional)
- [ ] Add/update unit tests for selectors
- [ ] Add integration tests
- [ ] Test backward compatibility
- [ ] Update CLAUDE.md if needed

---

## Part 4: Acceptance Criteria

### UI
1. Users can complete the upload-process-download workflow in fewer clicks
2. Visual design is clean and modern with consistent styling
3. Editor is intuitive for modifying attendee assignments
4. All existing functionality is preserved
5. All tests pass

### Core Attendee Feature
1. Core members (Core=1) are randomly selected first for initial attendee slots
2. Non-core members are available in editor dropdown for manual selection
3. Core members are visually distinguished in the editor
4. Configuration is simplified (no hardcoded ID weights)
5. Backward compatible with old NameList.csv format
6. All tests pass with 91%+ coverage maintained

---

## Technical Notes

### Key Files to Modify

```
src/saisonxform/
├── selectors.py          # Core attendee selection logic
├── config.py             # Remove ID weights, add core_fill_strategy
├── web/
│   ├── step_upload.py    # Minor: UI cleanup
│   ├── step_process.py   # Editor core/non-core distinction
│   ├── step_download.py  # Minor: UI cleanup
│   ├── sticky_header.py  # Simplify design
│   └── workflow_styles.py # CSS cleanup
data/reference/
├── NameList.csv          # Add Core column
└── config.toml           # Update configuration
templates/
└── report.html.j2        # Optional: core member indicator
tests/
└── test_selectors.py     # Update for core_ids parameter
```

### Running Tests

```bash
# Full test suite
poetry run pytest

# With coverage
poetry run pytest --cov --cov-report=term-missing

# Specific test file
poetry run pytest tests/test_selectors.py -v
```

### Code Quality

Before committing, run:
```bash
poetry run black src tests
poetry run ruff check src tests
poetry run mypy src
```

---

## Questions for Clarification

Before implementation, consider:

1. **Core Member Count**: How many core members should typically be defined? (Suggest: 4-8)
2. **Editor Grouping**: Should dropdown group Core/Non-Core, or just visually distinguish?
3. **Report Distinction**: Should HTML report show core member indicator?
4. **Sequential Mode**: Is sequential core selection needed, or just random?
5. **UI Consolidation**: Can Steps 2 and 3 be combined into one view?

---

*Created: 2026-01-25*
*For: Saison Transform v0.4.0*
