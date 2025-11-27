# Saison Transform Web Interface

A user-friendly web interface for processing financial transaction CSV files with drag-and-drop file upload and interactive data editing.

## 🚀 Quick Start

### Launch the Web Interface

```bash
# Option 1: Use the launch script
./run_web.sh

# Option 2: Run directly with Python
.venv/bin/python -m streamlit run web_app.py --server.port 8502
```

The interface will be available at:
- **Local**: http://localhost:8502
- **Network**: Check terminal output for network URL

## ✨ Features

### 📤 Upload & Process
- **Drag & Drop Interface**: Simply drag CSV files into the upload area
- **Multiple File Support**: Upload and process multiple files at once
- **Automatic Encoding Detection**: Handles UTF-8, UTF-8 BOM, and CP932 encodings
- **Batch Processing**: Process all uploaded files with one click
- **Progress Tracking**: Real-time progress bar and status updates

### ⚙️ Configuration (Sidebar)
- **Reference Data Loading**: Load attendee reference list from NameList.csv
- **Processing Parameters**:
  - Minimum attendees per transaction (1-10)
  - Maximum attendees per transaction (1-15)
- **ID Selection Weights**:
  - ID '2' weight (0-100%)
  - ID '1' weight (0-100%)
  - Automatically validates that weights sum to 100%

### ✏️ Edit Data
- **Interactive Table Editor**: Edit cells directly in the browser
- **Column Selection**: Choose which columns to display
- **Filter Options**: Show only relevant transactions (会議費/接待費)
- **Real-time Statistics**: View total rows, relevant transactions, and total amounts
- **Save Edits**: Preserve changes for download

### 💾 Download Results
- **CSV Download**: Download processed files with UTF-8 BOM encoding
- **HTML Report Download**: Generate and download formatted HTML reports
- **Pre-header Preservation**: Maintains any header rows from original files

## 📖 Usage Guide

### Step-by-Step Workflow

#### 1. **Load Attendee Reference**
   1. In the sidebar, verify the Reference Directory path (default: `../Reference`)
   2. Click **"Load Attendee Reference"** button
   3. Confirm success message shows number of attendees loaded

#### 2. **Configure Processing Parameters** (Optional)
   - Adjust min/max attendee counts using sliders
   - Set ID selection weights (default: 90% ID '2', 10% ID '1')
   - Ensure weights sum to 1.0 (100%)

#### 3. **Upload & Process Files**
   1. Go to **"📤 Upload & Process"** tab
   2. Drag and drop CSV files or click to browse
   3. Click **"🚀 Process All Files"** button
   4. Monitor progress bar and status messages
   5. Review processing summary (rows, relevant transactions, encoding)

#### 4. **Edit Data** (Optional)
   1. Go to **"✏️ Edit Data"** tab
   2. Select file from dropdown
   3. Choose display options:
      - Show only relevant transactions
      - Select specific columns
   4. Edit cells directly in the table
   5. Click **"💾 Save Edits"** to preserve changes

#### 5. **Download Results**
   1. Go to **"💾 Download Results"** tab
   2. For each processed file:
      - Click **"📥 Download CSV"** for processed data
      - Click **"📥 Download HTML Report"** for formatted report

## 📋 File Requirements

### Input CSV Files
Must contain these columns:
- `利用日` (Transaction Date)
- `ご利用店名及び商品名` (Store Name and Product Name)
- `利用金額` (Transaction Amount)
- `科目＆No.` (Category/Subject) - Used for filtering

### Reference File (NameList.csv)
Must contain these columns:
- `ID` (Unique Attendee Identifier)
- `Name` (Attendee Name)
- `Title` (Job Title)
- `Company` (Company Name)

Location: `../Reference/NameList.csv` (configurable in sidebar)

## 🎨 Interface Overview

### Tabs

#### Upload & Process Tab
```
┌─────────────────────────────────────┐
│  Drag and drop CSV files here      │
│  [Browse Files Button]              │
└─────────────────────────────────────┘

[🚀 Process All Files]

Processing Summary:
┌──────────┬──────┬──────────┬──────────┐
│ File     │ Rows │ Relevant │ Encoding │
├──────────┼──────┼──────────┼──────────┤
│ 202510...│ 150  │ 42       │ utf-8    │
└──────────┴──────┴──────────┴──────────┘
```

#### Edit Data Tab
```
Select file: [Dropdown ▼]

☐ Show only relevant transactions
Select columns: [Multi-select ▼]

┌────────────────────────────────────────┐
│ Interactive Data Table                  │
│ (Click cells to edit)                   │
└────────────────────────────────────────┘

[💾 Save Edits]

Statistics:
Total Rows: 150
Relevant: 42
Total Amount: ¥2,345,678
```

#### Download Results Tab
```
### file1.csv
[📥 Download CSV]    [📥 Download HTML Report]

### file2.csv
[📥 Download CSV]    [📥 Download HTML Report]
```

## 🔧 Troubleshooting

### Common Issues

**Problem**: "NameList.csv not found"
- **Solution**: Verify the Reference Directory path in sidebar
- Check that `NameList.csv` exists in that directory

**Problem**: "Missing required column '科目＆No.'"
- **Solution**: Ensure your CSV has the required columns
- Check that column names match exactly (Japanese characters)

**Problem**: "Weights should sum to 1.0"
- **Solution**: Adjust ID selection weight sliders so they add up to 100%

**Problem**: Web interface won't start
- **Solution**: Check if port 8502 is already in use
- Try changing the port: `streamlit run web_app.py --server.port 8503`

### Performance Tips

1. **Large Files**: For files with >1000 rows, consider:
   - Processing files one at a time
   - Using column selection in Edit tab
   - Filtering to relevant transactions only

2. **Multiple Files**: Process in batches if you have many files

3. **Encoding Issues**: If encoding detection fails:
   - Manually convert files to UTF-8 first
   - Check for special characters or corruption

## 🔒 Security Notes

- Files are processed in memory only
- Temporary files created in `/tmp/` are automatically cleaned up
- No data is stored permanently by the web interface
- Download files explicitly to save results

## 🆚 Web vs CLI Comparison

| Feature | Web Interface | CLI (`sf` command) |
|---------|--------------|-------------------|
| File Upload | Drag & Drop | Directory scanning |
| Batch Processing | ✅ | ✅ |
| Interactive Editing | ✅ | ❌ |
| Real-time Preview | ✅ | ❌ |
| Configuration | GUI Sliders | Config file / flags |
| File Archiving | ❌ | ✅ |
| Month Filtering | ❌ | ✅ |
| Best For | Quick edits, reviewing | Automation, batch jobs |

## 🎯 Use Cases

### Use Case 1: Quick Review and Edit
1. Upload a few transaction files
2. Process them with default settings
3. Review results in Edit tab
4. Make manual corrections
5. Download corrected files

### Use Case 2: Testing Different Parameters
1. Load reference data
2. Upload test files
3. Try different min/max attendee settings
4. Adjust ID selection weights
5. Compare results

### Use Case 3: One-off Processing
1. Upload files that don't fit the month naming pattern
2. Process without archiving
3. Download results immediately
4. No need to set up directory structure

## 📚 Additional Resources

- **CLI Documentation**: See `CLAUDE.md` for command-line usage
- **Configuration**: See `config.toml.example` for advanced settings
- **Project Overview**: See `README.md` for full project details

## 🐛 Known Limitations

1. **No Archiving**: Web interface doesn't move files to Archive directory
   - Use CLI for automated archiving workflows

2. **No Month Filtering**: Processes all uploaded files
   - Use CLI `--month` flag for selective processing

3. **Session State**: Data is lost on page refresh
   - Download results before closing browser

4. **Memory Usage**: Large files (>100MB) may cause performance issues
   - Process large files using CLI instead

## 💡 Tips & Tricks

1. **Keyboard Shortcuts** (in data editor):
   - `Tab` - Move to next cell
   - `Enter` - Confirm edit and move down
   - `Esc` - Cancel edit

2. **Column Width**: Click and drag column headers to resize

3. **Sorting**: Click column headers to sort data

4. **Filter First**: Use "Show only relevant" before editing to focus on important rows

5. **Save Often**: Click "Save Edits" frequently to preserve changes

## 🔄 Updating the Interface

To get the latest version:

```bash
cd /home/teabagger/dev/projects/saisonxform
git pull
.venv/bin/pip install --upgrade streamlit
```

Then restart the web interface.

---

**Questions or Issues?**

- Check `CLAUDE.md` for project-wide documentation
- Review error messages in the web interface
- Try the CLI for comparison: `sf --help`
