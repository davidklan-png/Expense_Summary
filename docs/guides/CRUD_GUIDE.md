# NameList.csv CRUD Operations Guide

The Saison Transform web interface now includes a complete CRUD (Create, Read, Update, Delete) interface for managing the attendee database (NameList.csv) directly from your browser.

## 🎯 Overview

All attendee management happens in the **"👥 Manage Attendees"** tab, which provides:

- ✅ **View/Edit** existing attendees
- ➕ **Add** new attendees
- 🗑️ **Delete** attendees
- 💾 **Export** data in multiple formats
- 🔍 **Search & Filter** capabilities
- 🔄 **Automatic backup** before saving

## 📋 Features

### 1. View & Edit Attendees

**Location**: Manage Attendees → View/Edit tab

**Features**:
- Interactive table with all attendee data
- Click any cell to edit Name, Company, or Title
- ID field is read-only (auto-managed)
- Real-time validation
- Bulk editing support

**How to Edit**:
1. Click on any cell in the table
2. Type your changes
3. Press Enter or click outside to confirm
4. Click **"💾 Save Changes"** to persist to file
5. A backup file (`NameList_backup.csv`) is created automatically

**Column Configuration**:
- **ID**: Read-only, automatically assigned
- **Company**: Required text field
- **Title**: Required text field
- **Name**: Required text field

### 2. Add New Attendees

**Location**: Manage Attendees → Add New tab

**Features**:
- Auto-incremented ID assignment
- Form validation
- Immediate save to file
- Automatic backup

**How to Add**:
1. Go to "Add New" tab
2. Fill in the form:
   - **ID**: Auto-filled (next available ID)
   - **Name**: Enter full name (e.g., 山田太郎)
   - **Company**: Enter company name (e.g., ABC株式会社)
   - **Title**: Enter job title (e.g., 部長)
3. Click **"➕ Add Attendee"**
4. New attendee is immediately saved to NameList.csv

**Validation**:
- All fields except ID are required
- Empty submissions will show an error
- ID is automatically calculated (highest current ID + 1)

### 3. Delete Attendees

**Location**: Manage Attendees → Delete tab

**Features**:
- Multi-select deletion
- Confirmation before delete
- Permanent removal from NameList.csv
- Automatic backup before deletion

**How to Delete**:
1. Go to "Delete" tab
2. Select one or more attendees from the dropdown
   - Format: "ID X: Name (Company)"
3. Review the warning message
4. Click **"🗑️ Confirm Delete"**
5. Attendees are permanently removed from file

**Warning**:
⚠️ Deletion is permanent! A backup is created, but deleted attendees cannot be easily restored through the UI.

### 4. Search & Filter

**Location**: Available in all tabs

**Search Bar**:
- Search by Name, Company, or Title
- Case-insensitive matching
- Real-time filtering

**Company Filter**:
- Dropdown with all companies
- Select "All" to show everyone
- Combines with search for precise filtering

**Examples**:
- Search "Manulife" → Shows all Manulife employees
- Search "Manager" → Shows all managers regardless of company
- Company filter "Deloitte" → Shows only Deloitte employees

### 5. Export Data

**Location**: Manage Attendees → Export tab

**Available Formats**:

#### 📥 CSV Export
- UTF-8 encoded
- Compatible with Excel and other tools
- Preserves all data

#### 📥 Excel Export
- `.xlsx` format
- Single sheet named "Attendees"
- Formatted for easy reading

#### 📥 JSON Export
- Structured data format
- UTF-8 with proper Japanese character support
- Useful for integrations

**Export applies to**:
- Current filtered/searched data
- If no filters, exports all attendees

## 📊 Statistics Dashboard

At the top of the Manage Attendees tab, you'll see:

| Metric | Description |
|--------|-------------|
| Total Attendees | Current count in database |
| Companies | Number of unique companies |
| Next ID | ID that will be assigned to next new attendee |
| 🔄 Refresh Data | Reload NameList.csv from disk |

## 🔄 Workflow Examples

### Example 1: Add a New Employee

```
1. Load NameList.csv (sidebar)
2. Go to "Manage Attendees" tab
3. Click "Add New" sub-tab
4. Fill in form:
   - Name: 田中美咲
   - Company: GHI株式会社
   - Title: 係長
5. Click "➕ Add Attendee"
6. Success! ID 67 assigned automatically
```

### Example 2: Update Employee Title

```
1. Load NameList.csv
2. Go to "Manage Attendees" → "View/Edit"
3. Search for employee name
4. Click on Title cell
5. Change value (e.g., "Manager" → "Sr Manager")
6. Click "💾 Save Changes"
7. Backup created, file updated
```

### Example 3: Clean Up Old Entries

```
1. Load NameList.csv
2. Go to "Delete" tab
3. Select multiple attendees to remove:
   - ID 50: Person A (Company X)
   - ID 51: Person B (Company Y)
4. Review warning
5. Click "🗑️ Confirm Delete"
6. Backup created, entries removed
```

### Example 4: Export Manulife Employees

```
1. Load NameList.csv
2. Use Company filter → Select "Manulife"
3. Shows 15 filtered results
4. Go to "Export" tab
5. Click "📥 Download as Excel"
6. File contains only Manulife employees
```

## 🔒 Data Safety Features

### Automatic Backups

Every save operation creates a backup:
- **Location**: Same directory as NameList.csv
- **Filename**: `NameList_backup.csv`
- **Timing**: Created BEFORE any write operation
- **Overwrite**: Each save overwrites previous backup

To restore from backup:
```bash
cd /home/teabagger/202511/Reference
cp NameList_backup.csv NameList.csv
```

### File Persistence

Changes are saved to disk immediately when you:
- Click "Save Changes" (Edit tab)
- Click "Add Attendee" (Add tab)
- Click "Confirm Delete" (Delete tab)

### Refresh Data

If the file is modified externally:
1. Click **"🔄 Refresh Data"** button
2. Reloads latest version from disk
3. Discards any unsaved in-memory changes

## 🎨 User Interface

### Navigation

```
Saison Transform Web Interface
├── 👥 Manage Attendees (NEW!)
│   ├── 📋 View/Edit
│   ├── ➕ Add New
│   ├── 🗑️ Delete
│   └── 💾 Export
├── 📤 Upload & Process
├── ✏️ Edit Data
└── 💾 Download Results
```

### Keyboard Shortcuts (in tables)

| Key | Action |
|-----|--------|
| Click | Start editing cell |
| Enter | Confirm edit, move down |
| Tab | Confirm edit, move right |
| Esc | Cancel edit |

### Visual Feedback

- ✅ **Green boxes**: Success messages
- ❌ **Red boxes**: Error messages
- ⚠️ **Yellow boxes**: Warnings
- ℹ️ **Blue boxes**: Information

## 🐛 Troubleshooting

### "No file path set. Load NameList.csv first."

**Cause**: NameList.csv not loaded
**Solution**:
1. Go to sidebar
2. Verify Reference Directory path
3. Click "📂 Load Attendee Reference"

### Changes don't persist after refresh

**Cause**: Didn't click "Save Changes"
**Solution**:
- Always click the save button after edits
- Look for success message before leaving page

### Can't edit ID field

**Cause**: ID is read-only by design
**Solution**:
- IDs are auto-managed
- To change ID, delete and re-add attendee

### Deleted wrong person

**Solution**:
1. Don't panic - backup exists
2. Go to Reference directory
3. Copy `NameList_backup.csv` to `NameList.csv`
4. Click "🔄 Refresh Data" in web interface

## 💡 Tips & Best Practices

### Daily Operations

1. **Load once**: Load NameList.csv at start of session
2. **Search first**: Use search before scrolling through long lists
3. **Save often**: Click save after each edit batch
4. **Check backup**: Verify backup file exists after major changes

### Bulk Operations

1. **Add multiple**: Use "Add New" tab repeatedly for batch additions
2. **Delete multiple**: Select many at once in Delete tab
3. **Export filtered**: Use filters + export for targeted data

### Data Quality

1. **Consistent naming**: Use consistent company name formats
2. **Full titles**: Include complete job titles
3. **Japanese support**: Full Unicode support for Japanese text
4. **Check duplicates**: Search before adding to avoid duplicates

## 🔗 Integration with Transaction Processing

When you process transaction files:

1. Load NameList.csv in Manage Attendees tab
2. Attendee pool is used for ID selection
3. ID weighting (90% ID 2, 10% ID 1) applies
4. Only loaded attendees appear in processed transactions
5. Add new attendees mid-session without restarting

## 📈 Monitoring Changes

### Version Control (Optional)

For teams, consider adding NameList.csv to git:

```bash
cd /home/teabagger/202511/Reference
git add NameList.csv
git commit -m "Add 5 new Manulife employees"
git push
```

### Audit Trail

Backups provide a simple audit:
- `NameList.csv` - Current version
- `NameList_backup.csv` - Previous version
- Compare with: `diff NameList.csv NameList_backup.csv`

## 🚀 Quick Reference

| Task | Tab | Action |
|------|-----|--------|
| Edit name | View/Edit | Click cell → Type → Save |
| Add person | Add New | Fill form → Add Attendee |
| Remove person | Delete | Select → Confirm Delete |
| Find person | Any tab | Use search box |
| Filter by company | Any tab | Use company dropdown |
| Export all | Export | Choose format → Download |
| Reload file | Any tab | Click 🔄 Refresh Data |
| Check stats | Top of page | View metrics |

---

**Need more help?**

- Check [WEB_INTERFACE_GUIDE.md](./WEB_INTERFACE_GUIDE.md) for general interface help
- See [CLAUDE.md](./CLAUDE.md) for project overview
- Review CSV at: `/home/teabagger/202511/Reference/NameList.csv`
