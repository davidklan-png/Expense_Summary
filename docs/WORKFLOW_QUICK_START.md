# Workflow UI - Quick Start Guide

## For Developers

### Running the New UI

```bash
# Start the application
streamlit run web_app.py --server.port 8502

# Access at:
# http://localhost:8502
```

### File Structure

```
web_app.py                           # Main application (NEW)
web_app_old.py                       # Original tab-based UI (backup)
src/saisonxform/ui/
  ├── workflow_state.py              # State management
  ├── workflow_styles.py             # CSS & auto-scroll
  ├── sticky_header.py               # Header component
  ├── step_upload.py                 # Step 1: Upload
  ├── step_process.py                # Step 2: Process & Edit
  └── step_download.py               # Step 3: Download
```

### Key Components

#### 1. Workflow State
```python
from saisonxform.ui.workflow_state import (
    initialize_workflow_state,
    advance_to_next_step,
    reset_workflow,
)

# Initialize in main()
initialize_workflow_state()

# Advance when step completes
advance_to_next_step()  # Moves to next step + auto-scrolls

# Reset everything
reset_workflow()  # Returns to Step 1
```

#### 2. Sticky Header
```python
from saisonxform.ui.sticky_header import render_sticky_header

# Render at top of main()
render_sticky_header()
# Shows: Step indicator + Status + Reset button
```

#### 3. Steps
```python
from saisonxform.ui.step_upload import render_upload_step
from saisonxform.ui.step_process import render_process_edit_step
from saisonxform.ui.step_download import render_download_step

# Step 1: Upload
render_upload_step()

# Step 2: Process & Edit (pass callbacks)
render_process_edit_step(
    process_file_callback=process_file,
    render_editor_callback=render_editor
)

# Step 3: Download (pass report generator)
render_download_step(generate_report_callback=generate_report)
```

#### 4. Styles
```python
from saisonxform.ui.workflow_styles import (
    get_workflow_styles,
    get_auto_scroll_script
)

# Apply styles
st.markdown(get_workflow_styles(), unsafe_allow_html=True)

# Auto-scroll to step
st.markdown(get_auto_scroll_script("step-2"), unsafe_allow_html=True)
```

### Adding a New Step

1. **Create step component** (e.g., `step_export.py`):
```python
from .workflow_state import WorkflowStep, can_access_step

def render_export_step():
    if not can_access_step(WorkflowStep.EXPORT):
        st.markdown('<div class="section-locked">...</div>')
        return

    st.markdown('<div class="workflow-section" id="step-4">...')
    # Your step content
```

2. **Add to WorkflowStep enum** (`workflow_state.py`):
```python
class WorkflowStep(Enum):
    UPLOAD = 1
    PROCESS_EDIT = 2
    DOWNLOAD = 3
    EXPORT = 4  # NEW
```

3. **Update advance logic** (`workflow_state.py`):
```python
def advance_to_next_step():
    current = st.session_state.workflow_step
    if current == WorkflowStep.DOWNLOAD:
        set_current_step(WorkflowStep.EXPORT)
        st.session_state.scroll_to_step = "step-4"
```

4. **Add to sticky header** (`sticky_header.py`):
```python
steps = [
    {"step": WorkflowStep.UPLOAD, "number": 1, "label": "Upload"},
    {"step": WorkflowStep.PROCESS_EDIT, "number": 2, "label": "Review & Edit"},
    {"step": WorkflowStep.DOWNLOAD, "number": 3, "label": "Download"},
    {"step": WorkflowStep.EXPORT, "number": 4, "label": "Export"},  # NEW
]
```

5. **Render in main** (`web_app.py`):
```python
render_upload_step()
render_process_edit_step(...)
render_download_step(...)
render_export_step()  # NEW
```

### Customizing Styles

Edit `workflow_styles.py`:

```python
def get_workflow_styles():
    return """
    <style>
    /* Change primary color */
    :root {
        --primary-color: #ff6b6b;  /* Red theme */
    }

    /* Customize upload zone */
    .upload-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    /* Add custom step styles */
    .step-circle {
        animation: pulse 2s infinite;
    }
    </style>
    """
```

### Testing

```bash
# Run UI tests
.venv/bin/pytest tests/ui_tests/test_cross_browser.py -v

# Test specific step
.venv/bin/pytest tests/ui_tests/ -k "test_app_loads" -v

# Test Safari compatibility
.venv/bin/pytest tests/ui_tests/ -m safari -v
```

### Debugging

```python
# Check current state
print(f"Current step: {get_current_step()}")
print(f"Step completed: {st.session_state.step_completed}")
print(f"Processed files: {list(st.session_state.processed_files.keys())}")

# Force reset
if st.button("DEBUG: Force Reset"):
    reset_workflow()
    st.session_state.clear()
    st.rerun()
```

## For Users

### How to Use

1. **Upload Files** (Step 1)
   - Drag & drop CSV files or click to browse
   - Click "Continue to Review & Edit"

2. **Review & Edit** (Step 2)
   - Click "Process Files" button
   - Wait for progress bar to complete
   - Review data in table
   - Click "Continue to Download"

3. **Download Results** (Step 3)
   - Choose format: CSV, Excel, HTML, or ZIP
   - Download individual files or batch
   - Click "Process New Files" to start over

### Tips

- **Multiple Files**: Upload several files at once
- **Edit Data**: Toggle "Show all rows" to see full dataset
- **Attendees**: Expand attendee list to verify selection
- **Reset**: Click Reset button in header to start fresh

### Keyboard Shortcuts

- **Tab**: Navigate between buttons
- **Enter**: Click focused button
- **Escape**: Close expanders
- **Scroll**: Mouse wheel or trackpad to navigate steps

## Common Tasks

### Change Step Order

Edit `advance_to_next_step()` in `workflow_state.py`:

```python
def advance_to_next_step():
    if current == WorkflowStep.UPLOAD:
        set_current_step(WorkflowStep.DOWNLOAD)  # Skip process step
```

### Add Validation

In step component:

```python
def render_upload_step():
    uploaded_files = st.file_uploader(...)

    # Validate files
    for file in uploaded_files:
        if file.size > 10_000_000:  # 10MB limit
            st.error(f"{file.name} is too large")
            return

    if st.button("Continue"):
        advance_to_next_step()
```

### Custom Progress Indicator

```python
def render_process_edit_step(...):
    with st.spinner("Processing..."):
        for i, file in enumerate(files):
            st.progress((i + 1) / len(files))
            process_file(file)
```

### Add Step Summary

```python
def render_download_step(...):
    with st.expander("📊 Processing Summary"):
        st.write(f"Files processed: {len(processed_files)}")
        st.write(f"Total rows: {total_rows}")
        st.write(f"Errors: {error_count}")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Steps not unlocking | Check `can_access_step()` logic |
| Auto-scroll not working | Verify JavaScript enabled |
| Styling broken | Clear cache, reload CSS |
| Session state lost | Check session state initialization |
| Upload not working | Verify attendee list loaded |
| Processing fails | Check file format and encoding |

## Resources

- **Full Documentation**: `docs/WORKFLOW_UI.md`
- **UI Components**: `src/saisonxform/ui/`
- **Tests**: `tests/ui_tests/`
- **Original UI**: `web_app_old.py`

---

**Need Help?** Check [WORKFLOW_UI.md](WORKFLOW_UI.md) for detailed documentation.
