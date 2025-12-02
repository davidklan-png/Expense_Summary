# Three-Step Vertical Workflow UI

## Overview

The Saison Transform web interface has been redesigned with a modern, scroll-based three-step workflow that provides an intuitive and streamlined user experience.

## Design Principles

### 1. **Single-Page Vertical Flow**
- All steps appear on one continuous page
- Users scroll naturally through the workflow
- No tabs or modal dialogs to disrupt flow
- Progressive disclosure: each step unlocks after the previous completes

### 2. **Sticky Header with Step Indicator**
- Always visible at the top of the page
- Shows current step and completion status
- Visual progress indicators with icons
- Quick reset button for starting over

### 3. **8px Grid System**
- Consistent spacing using 8px base unit
- Clean, modern design with proper visual hierarchy
- Responsive layout for desktop, tablet, and mobile

### 4. **Progressive Disclosure**
- Step 2 appears locked until files are uploaded
- Step 3 appears locked until files are processed
- Clear visual feedback showing what needs to be done

### 5. **Auto-Scroll Behavior**
- Automatically scrolls to the next step when current step completes
- Smooth scroll animation for better UX
- Users always know where to focus next

## Workflow Steps

### Step 1: Upload 📤
**Purpose**: Upload transaction CSV files

**Features**:
- Large drag-and-drop zone with hover effects
- Multiple file upload support
- File list with size and status indicators
- Clear "Continue" button to advance

**User Journey**:
1. User lands on page, sees upload zone
2. Drags files or clicks to browse
3. Files appear in list with green checkmarks
4. Clicks "Continue to Review & Edit" button
5. Page auto-scrolls to Step 2

### Step 2: Review & Edit ✏️
**Purpose**: Process files and review/edit generated data

**Features**:
- Process button to start file processing
- Progress bar with real-time status
- File selector for multiple files
- Interactive data table with filtering
- Unique attendees list in expander
- Metrics showing row counts and attendees

**User Journey**:
1. User clicks "Process Files" button
2. Progress bar shows processing status
3. After processing, user reviews data in table
4. Can toggle "Show all rows" to see full dataset
5. Can expand attendees list to verify
6. Clicks "Continue to Download" button
7. Page auto-scrolls to Step 3

### Step 3: Download 💾
**Purpose**: Download results in various formats

**Features**:
- Summary metrics (files, transactions, attendees)
- Format selector: CSV, Excel, HTML, or ZIP
- Individual file downloads
- Batch ZIP download with all formats
- "Process New Files" button to reset workflow

**User Journey**:
1. User sees summary of processed data
2. Selects desired format
3. Downloads individual files or batch ZIP
4. Can reset to process more files

## Technical Architecture

### Component Structure

```
src/saisonxform/ui/
├── workflow_state.py       # State management
├── workflow_styles.py      # CSS styles
├── sticky_header.py        # Header component
├── step_upload.py          # Step 1 component
├── step_process.py         # Step 2 component
└── step_download.py        # Step 3 component
```

### State Management

**WorkflowStep Enum**:
- `UPLOAD` (1)
- `PROCESS_EDIT` (2)
- `DOWNLOAD` (3)

**Session State**:
```python
st.session_state.workflow_step          # Current step
st.session_state.step_completed        # Dict of completed steps
st.session_state.scroll_to_step        # Target for auto-scroll
st.session_state.uploaded_files_cache  # Cached uploaded files
st.session_state.processed_files       # Processed file data
```

### Key Functions

**workflow_state.py**:
- `initialize_workflow_state()` - Initialize state
- `get_current_step()` - Get current step
- `advance_to_next_step()` - Move to next step
- `reset_workflow()` - Reset to beginning
- `can_access_step(step)` - Check if step is accessible
- `mark_step_complete(step)` - Mark step as done

**Sticky Header**:
- Displays step indicator with 3 circles
- Shows status for each step (Complete, In Progress, Ready, Locked)
- Reset button to start over
- Responsive design for mobile

**Auto-Scroll**:
- JavaScript injection for smooth scrolling
- `scroll_to_step` state variable triggers scroll
- Scroll target IDs: `step-1`, `step-2`, `step-3`

## CSS Architecture

### Design Tokens
- **Colors**: Primary (#1f77b4), Success (#28a745), Warning (#ffc107), Danger (#dc3545)
- **Spacing**: 8px grid (xs=8px, sm=16px, md=24px, lg=32px, xl=48px, 2xl=64px)
- **Border Radius**: 8px standard, 16px for containers
- **Shadows**: Layered depth (sm, md, lg)

### Key CSS Classes

**Workflow Structure**:
- `.sticky-header` - Fixed header at top
- `.workflow-section` - Each step container
- `.section-locked` - Disabled step with overlay

**Components**:
- `.upload-container` - Drag & drop zone
- `.progress-container` - Processing status
- `.file-list` - Uploaded file list
- `.cta-container` - Call-to-action button wrapper

**Animations**:
- `fadeSlideIn` - Smooth entrance for sections
- `pulse` - Loading indicators
- Smooth hover transitions on interactive elements

## Safari Compatibility

### Regex Fix Maintained
- Network URLs still use `st.code()` instead of markdown links
- Prevents Safari "invalid group specifier name" error
- All markdown rendering is Safari-safe

### WebKit Testing
- UI tests validate step indicator rendering
- Touch-friendly for iPad
- Responsive breakpoints tested

## Responsive Design

### Breakpoints
- **Desktop** (>768px): Horizontal step indicator, full sidebar
- **Tablet/Mobile** (≤768px): Vertical step indicator, collapsible sidebar

### Mobile Optimizations
- Sticky header stacks vertically
- Step indicators in column layout
- Upload zone padding reduced
- Touch-friendly button sizes

## User Flow Examples

### Happy Path
1. **Landing** → User sees Step 1 (Upload)
2. **Upload** → Drags 3 files → Clicks "Continue"
3. **Auto-scroll** → Page scrolls to Step 2
4. **Process** → Clicks "Process 3 Files" → Progress bar shows status
5. **Review** → Sees data table → Checks attendees
6. **Continue** → Clicks "Continue to Download"
7. **Auto-scroll** → Page scrolls to Step 3
8. **Download** → Selects "All Formats (ZIP)" → Downloads
9. **Reset** → Clicks "Process New Files" → Returns to Step 1

### Error Handling
- **No attendee list**: Warning in Step 1, blocks upload
- **Processing error**: Error message, file marked as failed
- **Empty file**: Error message, user can re-upload
- **Network error**: Toast notification, user can retry

## Performance Optimizations

### Caching
- Uploaded files cached in session state
- Processed data stored to avoid reprocessing
- Attendee reference loaded once

### Progressive Loading
- Steps only render when accessible
- Data tables use lazy loading
- File processing shows real-time progress

### Memory Management
- Files processed one at a time
- Temporary files cleaned up immediately
- Session state cleared on reset

## Accessibility

### WCAG Compliance
- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus indicators on all controls

### Screen Reader Support
- Step status announced
- Progress bar with aria-live
- Error messages read aloud
- Button labels descriptive

## Migration Notes

### Differences from Old UI
**Old UI** (Tab-based):
- 4 tabs: Upload & Process, Preview & Edit, Download, Manage Attendees
- User switches between tabs manually
- All tabs always visible
- Processing happened in tab 1

**New UI** (Vertical workflow):
- 3 sequential steps on one page
- Progressive disclosure, steps unlock
- Auto-scroll to guide user
- Processing integrated into Step 2

### Backward Compatibility
- Old `web_app.py` saved as `web_app_old.py`
- All backend logic unchanged
- Attendee management moved to sidebar
- Same file formats and processing

## Deployment

### Requirements
No new dependencies required. The redesign uses:
- Streamlit (existing)
- Custom CSS (no external libraries)
- Session state (built-in)

### Configuration
No configuration changes needed. All settings remain in:
- `.streamlit/config.toml`
- `data/reference/config.toml`

### Testing
Run UI tests to verify:
```bash
./run_ui_tests.sh chromium all
./run_ui_tests.sh webkit safari
```

## Future Enhancements

### Potential Additions
1. **Keyboard Shortcuts**: Alt+1/2/3 to jump to steps
2. **Undo/Redo**: Edit history for data changes
3. **Bulk Edit**: Edit multiple rows at once
4. **Real-time Validation**: Validate data as user types
5. **Template System**: Save/load processing configs
6. **Export History**: Track all downloads
7. **Collaborative Editing**: Multi-user support

### Design Iterations
1. **Dark Mode**: Theme toggle in sidebar
2. **Compact Mode**: Reduced spacing option
3. **Wizard Mode**: Modal-based alternative
4. **Dashboard View**: Analytics after Step 3

## Troubleshooting

### Common Issues

**Step won't unlock**:
- Check previous step is marked complete
- Verify files were uploaded/processed
- Check browser console for errors

**Auto-scroll not working**:
- Ensure JavaScript is enabled
- Check for console errors
- Try manual scroll

**Styling issues**:
- Clear browser cache
- Check for CSS conflicts
- Verify custom CSS loaded

**Reset button not working**:
- Check session state is initialized
- Verify button callback is registered
- Look for errors in server logs

## Support

For issues or questions:
1. Check server logs: `BashOutput` for Streamlit process
2. Review browser console for JavaScript errors
3. Test with UI test suite
4. Open GitHub issue with screenshots

---

**Version**: 1.0.0
**Last Updated**: 2025-12-02
**Author**: Claude (Anthropic)
**Status**: ✅ Production Ready
