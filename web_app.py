"""Streamlit Web Interface for Saison Transform.

Interactive web application for uploading, processing, and editing
financial transaction CSV files with attendee management and preview.
"""

import io
import sys
import zipfile
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from saisonxform.config import Config
from saisonxform.io import read_csv_with_detection, write_csv_utf8_bom
from saisonxform.selectors import estimate_attendee_count, sample_attendee_ids
from saisonxform.reporting import generate_html_report, get_unique_attendees

# Page configuration
st.set_page_config(
    page_title="Saison Transform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        padding: 1rem 0;
    }
    .file-upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .preview-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = {}
    if "preview_data" not in st.session_state:
        st.session_state.preview_data = {}
    if "edited_data" not in st.session_state:
        st.session_state.edited_data = {}
    if "config" not in st.session_state:
        try:
            st.session_state.config = Config()
        except Exception:
            st.session_state.config = None
    if "attendee_ref" not in st.session_state:
        st.session_state.attendee_ref = None
    if "attendee_ref_path" not in st.session_state:
        st.session_state.attendee_ref_path = None
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "current_preview_file" not in st.session_state:
        st.session_state.current_preview_file = None

    # Auto-load attendee reference on first run
    if st.session_state.attendee_ref is None:
        default_ref_path = Path("/home/teabagger/202511/Reference/NameList.csv")
        if default_ref_path.exists():
            try:
                attendee_ref = load_attendee_reference(default_ref_path)
                if attendee_ref is not None:
                    st.session_state.attendee_ref = attendee_ref
                    st.session_state.attendee_ref_path = default_ref_path
            except Exception:
                # Silently fail - user can manually load later
                pass


def load_attendee_reference(reference_path: Path) -> Optional[pd.DataFrame]:
    """Load attendee reference list from NameList.csv."""
    if reference_path.exists():
        df = pd.read_csv(reference_path, encoding="utf-8")
        st.session_state.attendee_ref_path = reference_path
        return df
    return None


def save_attendee_reference(df: pd.DataFrame, reference_path: Path) -> bool:
    """Save attendee reference list to NameList.csv."""
    try:
        if reference_path.exists():
            backup_path = reference_path.parent / f"{reference_path.stem}_backup.csv"
            import shutil
            shutil.copy2(reference_path, backup_path)
        df.to_csv(reference_path, index=False, encoding="utf-8")
        return True
    except Exception as e:
        st.error(f"Error saving NameList.csv: {e}")
        return False


def get_next_id(df: pd.DataFrame) -> int:
    """Get the next available ID."""
    if df.empty:
        return 1
    max_id = df["ID"].max()
    return int(max_id) + 1


def reset_session():
    """Reset the session by clearing preview and processed data."""
    st.session_state.preview_data = {}
    st.session_state.processed_data = {}
    st.session_state.current_preview_file = None
    if "uploaded_files_cache" in st.session_state:
        st.session_state.uploaded_files_cache = {}


def recalculate_attendee_count(row: pd.Series) -> int:
    """Recalculate 人数 based on non-empty ID fields."""
    count = 0
    for i in range(1, 9):
        id_val = row.get(f"ID{i}", "")
        if id_val and str(id_val).strip() != "":
            count += 1
    return count




def process_uploaded_file(
    uploaded_file, min_attendees: int = 2, max_attendees: int = 8,
    id_2_weight: float = 0.9, id_1_weight: float = 0.1,
    use_amount_based: bool = False, amount_brackets: Optional[dict] = None,
    cost_per_person: int = 3000
) -> tuple[pd.DataFrame, str, list]:
    """Process an uploaded CSV file with optional amount-based attendee estimation."""
    temp_path = Path(f"/tmp/{uploaded_file.name}")
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    df, encoding, pre_header_rows = read_csv_with_detection(temp_path)
    temp_path.unlink()

    if df.empty:
        raise ValueError("File is empty")

    # Keep ALL rows from input (including summary rows, cardholder names, etc.)
    # Only identify which rows are relevant transactions for attendee assignment

    attendee_ref = st.session_state.attendee_ref
    if attendee_ref is None:
        raise ValueError("Attendee reference not loaded")

    available_ids = attendee_ref["ID"].astype(str).tolist()

    # Create mask for relevant transactions (会議費/接待費) with valid dates
    has_date = df["利用日"].notna() if "利用日" in df.columns else pd.Series([False] * len(df))
    has_subject = df["科目＆No."].notna() if "科目＆No." in df.columns else pd.Series([False] * len(df))

    # Relevant = has date AND has subject AND (会議費 OR 接待費)
    relevant_mask = has_date & has_subject & df["科目＆No."].str.contains("会議費|接待費", na=False, regex=True)

    # Initialize columns
    df["人数"] = ""
    for i in range(1, 9):
        df[f"ID{i}"] = ""

    # Process relevant transactions
    if relevant_mask.sum() > 0:
        for idx in df[relevant_mask].index:
            amount = df.loc[idx, "利用金額"]

            # Use amount-based logic if enabled
            brackets_to_use = amount_brackets if use_amount_based else None

            count = estimate_attendee_count(
                amount,
                min_attendees=min_attendees,
                max_attendees=max_attendees,
                amount_brackets=brackets_to_use,
                cost_per_person=cost_per_person
            )
            df.loc[idx, "人数"] = count

            ids_result = sample_attendee_ids(
                count=count, available_ids=available_ids,
                id_2_weight=id_2_weight, id_1_weight=id_1_weight, return_dict=True
            )
            assert isinstance(ids_result, dict)
            for i in range(1, 9):
                col_name = f"ID{i}"
                df.loc[idx, col_name] = ids_result[col_name]

    # Remove unwanted columns
    columns_to_drop = ["本人・家族区分", "締前入金区分"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    # Add blank 備考 column at the end
    if "備考" not in df.columns:
        df["備考"] = ""

    return df, encoding, pre_header_rows


def render_preview_editor(filename: str):
    """Render the preview editor for a specific file."""
    if filename not in st.session_state.preview_data:
        st.error("Preview data not found")
        return

    data_dict = st.session_state.preview_data[filename]
    df = data_dict["data"].copy()
    encoding = data_dict["encoding"]
    pre_header = data_dict["pre_header"]
    attendee_ref = st.session_state.attendee_ref

    st.markdown(f'<div class="preview-box"><h3>📋 Preview & Edit: {filename}</h3></div>', unsafe_allow_html=True)

    # Show encoding info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        relevant_count = (df["人数"] != "").sum()
        st.metric("Relevant Transactions", relevant_count)
    with col3:
        st.metric("Encoding", encoding)

    # Filter to show only relevant transactions
    relevant_mask = df["人数"] != ""
    if relevant_mask.sum() == 0:
        st.warning("⚠️ No relevant transactions (会議費/接待費) found in this file.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to File List", key=f"back_{filename}"):
                del st.session_state.preview_data[filename]
                st.session_state.current_preview_file = None
                st.rerun()
        return

    display_df = df[relevant_mask].copy()

    # Get attendee ID options for dropdown
    available_ids = [""] + attendee_ref["ID"].astype(str).tolist()
    attendee_dict = {str(row["ID"]): f"{row['ID']}: {row['Name']} ({row['Company']})"
                     for _, row in attendee_ref.iterrows()}
    attendee_dict[""] = ""

    st.subheader("🔧 Edit Attendee IDs")
    st.info("💡 Click on ID cells to edit attendee assignments. 人数 will auto-update.")

    # Select columns to display in editor - include 備考 after ID8
    id_cols = [f"ID{i}" for i in range(1, 9)]
    display_cols = ["利用日", "ご利用店名及び商品名", "利用金額", "人数"] + id_cols + ["備考"]
    display_cols = [col for col in display_cols if col in display_df.columns]

    # Create editable dataframe
    edited_df = st.data_editor(
        display_df[display_cols],
        width="stretch",
        num_rows="fixed",
        hide_index=False,
        column_config={
            "利用日": st.column_config.TextColumn("利用日", disabled=True),
            "ご利用店名及び商品名": st.column_config.TextColumn("店名", disabled=True, width="medium"),
            "利用金額": st.column_config.NumberColumn("金額", disabled=True),
            "人数": st.column_config.NumberColumn("人数", disabled=True),
            **{f"ID{i}": st.column_config.SelectboxColumn(
                f"ID{i}",
                options=available_ids,
                required=False
            ) for i in range(1, 9)},
            "備考": st.column_config.TextColumn("備考", width="medium", required=False),
        },
        key=f"preview_editor_{filename}"
    )

    # Auto-recalculate 人数 when IDs change
    if not edited_df.equals(display_df[display_cols]):
        st.info("🔄 Recalculating attendee counts...")
        for idx in edited_df.index:
            # Recalculate 人数
            new_count = recalculate_attendee_count(edited_df.loc[idx])
            edited_df.loc[idx, "人数"] = new_count

        # Update the main dataframe
        for col in display_cols:
            if col in edited_df.columns:
                df.loc[edited_df.index, col] = edited_df[col]

        # Update preview data
        st.session_state.preview_data[filename]["data"] = df

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("✅ Confirm & Save", type="primary", key=f"confirm_{filename}", width="stretch"):
            # Move to processed data
            st.session_state.processed_data[filename] = {
                "data": df,
                "encoding": encoding,
                "pre_header": pre_header
            }
            # Clear preview
            del st.session_state.preview_data[filename]
            st.session_state.current_preview_file = None
            st.success(f"✅ {filename} saved to processed data!")
            st.rerun()

    with col2:
        if st.button("⬅️ Back to File List", key=f"back2_{filename}", width="stretch"):
            del st.session_state.preview_data[filename]
            st.session_state.current_preview_file = None
            st.rerun()

    # Show attendee summary
    st.subheader("👥 Attendee Summary")
    unique_attendees_df = get_unique_attendees(df, attendee_ref)
    if not unique_attendees_df.empty:
        st.dataframe(unique_attendees_df, width="stretch", hide_index=True)
    else:
        st.info("No attendees assigned yet")


def render_attendee_management():
    """Render the attendee management CRUD interface."""
    st.header("👥 Attendee Management")

    if st.session_state.attendee_ref is None:
        st.info("📝 Please load the attendee reference first using the sidebar.")
        return

    df = st.session_state.attendee_ref.copy()

    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Attendees", len(df))
    with col2:
        unique_companies = df["Company"].nunique()
        st.metric("Companies", unique_companies)
    with col3:
        next_id = get_next_id(df)
        st.metric("Next ID", next_id)
    with col4:
        if st.button("🔄 Refresh Data"):
            if st.session_state.attendee_ref_path:
                reloaded = load_attendee_reference(st.session_state.attendee_ref_path)
                if reloaded is not None:
                    st.session_state.attendee_ref = reloaded
                    st.success("✅ Data refreshed from file")
                    st.rerun()

    # Search and filter
    st.subheader("🔍 Search & Filter")
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search by Name, Company, or Title", "")
    with col2:
        company_filter = st.selectbox(
            "Filter by Company",
            ["All"] + sorted(df["Company"].unique().tolist())
        )

    # Apply filters
    filtered_df = df.copy()
    if search_term:
        mask = (
            filtered_df["Name"].str.contains(search_term, case=False, na=False) |
            filtered_df["Company"].str.contains(search_term, case=False, na=False) |
            filtered_df["Title"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if company_filter != "All":
        filtered_df = filtered_df[filtered_df["Company"] == company_filter]

    st.info(f"Showing {len(filtered_df)} of {len(df)} attendees")

    # CRUD Operations Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View/Edit", "➕ Add New", "🗑️ Delete", "💾 Export"])

    with tab1:
        st.subheader("View and Edit Attendees")

        edited_df = st.data_editor(
            filtered_df,
            width="stretch",
            num_rows="fixed",
            hide_index=False,
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "Company": st.column_config.TextColumn("Company", required=True),
                "Title": st.column_config.TextColumn("Title", required=True),
                "Name": st.column_config.TextColumn("Name", required=True),
            },
            key="attendee_editor"
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("💾 Save Changes", type="primary", width="stretch"):
                if not search_term and company_filter == "All":
                    st.session_state.attendee_ref = edited_df
                else:
                    for idx, row in edited_df.iterrows():
                        df.loc[df["ID"] == row["ID"], ["Company", "Title", "Name"]] = [
                            row["Company"], row["Title"], row["Name"]
                        ]
                    st.session_state.attendee_ref = df

                if st.session_state.attendee_ref_path:
                    if save_attendee_reference(st.session_state.attendee_ref, st.session_state.attendee_ref_path):
                        st.success("✅ Changes saved successfully!")
                        st.rerun()
                else:
                    st.error("❌ No file path set. Load NameList.csv first.")

        with col2:
            st.info("💡 Edit cells directly in the table above. Click 'Save Changes' to persist to file.")

    with tab2:
        st.subheader("Add New Attendee")

        with st.form("add_attendee_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_id = st.number_input("ID", value=get_next_id(df), min_value=1, disabled=True)
                new_name = st.text_input("Name *", placeholder="e.g., 山田太郎")

            with col2:
                new_company = st.text_input("Company *", placeholder="e.g., ABC株式会社")
                new_title = st.text_input("Title *", placeholder="e.g., 部長")

            submitted = st.form_submit_button("➕ Add Attendee", type="primary", width="stretch")

            if submitted:
                if not new_name or not new_company or not new_title:
                    st.error("❌ Please fill in all required fields (Name, Company, Title)")
                else:
                    new_row = pd.DataFrame({
                        "ID": [new_id],
                        "Company": [new_company],
                        "Title": [new_title],
                        "Name": [new_name]
                    })

                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    st.session_state.attendee_ref = updated_df

                    if st.session_state.attendee_ref_path:
                        if save_attendee_reference(updated_df, st.session_state.attendee_ref_path):
                            st.success(f"✅ Added attendee with ID {new_id}")
                            st.rerun()
                    else:
                        st.error("❌ No file path set. Load NameList.csv first.")

    with tab3:
        st.subheader("Delete Attendees")
        st.warning("⚠️ Deleted attendees will be permanently removed from NameList.csv")

        delete_options = [
            f"ID {row['ID']}: {row['Name']} ({row['Company']})"
            for _, row in filtered_df.iterrows()
        ]

        selected_to_delete = st.multiselect("Select attendees to delete", delete_options)

        if selected_to_delete:
            st.error(f"⚠️ You are about to delete {len(selected_to_delete)} attendee(s)")

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🗑️ Confirm Delete", type="secondary", width="stretch"):
                    ids_to_delete = []
                    for item in selected_to_delete:
                        id_str = item.split(":")[0].replace("ID ", "")
                        ids_to_delete.append(int(id_str))

                    updated_df = df[~df["ID"].isin(ids_to_delete)].copy()
                    st.session_state.attendee_ref = updated_df

                    if st.session_state.attendee_ref_path:
                        if save_attendee_reference(updated_df, st.session_state.attendee_ref_path):
                            st.success(f"✅ Deleted {len(ids_to_delete)} attendee(s)")
                            st.rerun()
                    else:
                        st.error("❌ No file path set. Load NameList.csv first.")

    with tab4:
        st.subheader("Export Attendee Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            csv_buffer = io.StringIO()
            filtered_df.to_csv(csv_buffer, index=False, encoding="utf-8")
            csv_data = csv_buffer.getvalue()

            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="attendees.csv",
                mime="text/csv",
                width="stretch"
            )

        with col2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='Attendees')
            excel_data = excel_buffer.getvalue()

            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name="attendees.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch"
            )

        with col3:
            json_data = filtered_df.to_json(orient="records", force_ascii=False, indent=2)

            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name="attendees.json",
                mime="application/json",
                width="stretch"
            )


def main():
    """Main application entry point."""
    initialize_session_state()

    # Auto-load attendee reference on first run
    if st.session_state.attendee_ref is None:
        try:
            # Try data/reference/NameList.csv first (project structure)
            ref_path = Path("data/reference/NameList.csv")
            if ref_path.exists():
                attendee_ref = load_attendee_reference(ref_path)
                if attendee_ref is not None:
                    st.session_state.attendee_ref = attendee_ref
                    st.session_state.attendee_ref_path = ref_path
        except Exception:
            pass  # Will be loaded manually if needed

    # Header
    st.markdown('<div class="main-header">💳 Saison Transform</div>', unsafe_allow_html=True)
    st.markdown("**Quick Start:** Upload files → Preview & edit → Download results")

    # Sidebar for configuration (collapsed by default)
    with st.sidebar:
        st.header("⚙️ Settings")

        # Attendee list status (always visible)
        if st.session_state.attendee_ref is not None:
            st.success(f"✅ {len(st.session_state.attendee_ref)} attendees loaded")
            if st.session_state.attendee_ref_path:
                st.caption(f"📄 {st.session_state.attendee_ref_path.name}")
        else:
            st.warning("⚠️ No attendee list loaded")

        # Reference data settings (collapsible)
        with st.expander("📂 Reference Data", expanded=False):
            reference_dir = st.text_input(
                "Reference Directory",
                value=str(Path("data/reference")),
                help="Directory containing NameList.csv"
            )

            if st.button("🔄 Reload Attendee List"):
                try:
                    ref_path = Path(reference_dir) / "NameList.csv"
                    attendee_ref = load_attendee_reference(ref_path)
                    if attendee_ref is not None:
                        st.session_state.attendee_ref = attendee_ref
                        st.session_state.attendee_ref_path = ref_path
                        st.success(f"✅ Loaded {len(attendee_ref)} attendees")
                        st.rerun()
                    else:
                        st.error("❌ NameList.csv not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # Processing parameters (collapsible)
        with st.expander("🔧 Processing Parameters", expanded=False):
            # Load config values
            config = st.session_state.config
            use_amount_based = False
            amount_brackets = None
            cost_per_person = 3000

            if config and config.amount_based_attendees:
                use_amount_based = True
                amount_brackets = config.amount_based_attendees.get("brackets")
                cost_per_person = config.amount_based_attendees.get("cost_per_person", 3000)

            # Amount-based toggle
            use_amount_based = st.checkbox(
                "Enable Amount-Based Attendee Estimation",
                value=use_amount_based,
                help="Use transaction amounts to determine attendee counts"
            )

            if use_amount_based:
                st.info("📊 Using amount-based brackets from config")
                if amount_brackets:
                    st.caption(f"💰 Cost per person: ¥{cost_per_person:,}")
                    for (min_amt, max_amt), attendee_range in amount_brackets.items():
                        st.text(f"¥{min_amt:,}-{max_amt:,}: {attendee_range['min']}-{attendee_range['max']} people")
                else:
                    st.warning("⚠️ Amount brackets not configured in config.toml")
            else:
                st.info("🎲 Using random attendee selection")

            min_attendees = st.slider(
                "Min Attendees",
                1, 10,
                config.min_attendees if config else 2,
                help="Minimum attendees (used when amount-based is disabled)"
            )
            max_attendees = st.slider(
                "Max Attendees",
                1, 15,
                config.max_attendees if config else 8,
                help="Maximum attendees (also caps amount-based fallback)"
            )

            st.divider()

            # Get weights from config
            default_weights = {"2": 0.9, "1": 0.1}
            if config and config.primary_id_weights:
                default_weights = config.primary_id_weights

            id_2_weight = st.slider(
                "ID '2' Weight",
                0.0, 1.0,
                float(default_weights.get("2", 0.9)),
                0.05,
                help="Probability of selecting ID '2' as primary attendee"
            )
            id_1_weight = st.slider(
                "ID '1' Weight",
                0.0, 1.0,
                float(default_weights.get("1", 0.1)),
                0.05,
                help="Probability of selecting ID '1' as primary attendee"
            )

            if abs((id_2_weight + id_1_weight) - 1.0) > 0.01:
                st.warning("⚠️ Weights should sum to 1.0")

            st.caption("💡 Edit `data/reference/config.toml` to change default settings")

    # Main content area - workflow-focused tab order
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Process", "✏️ Preview & Edit", "💾 Download Results", "👥 Manage Attendees"])

    with tab1:
        st.header("📤 Upload & Process Files")

        # Check if attendee list is loaded
        if st.session_state.attendee_ref is None:
            st.error("⚠️ **Attendee list not loaded!** Please load NameList.csv from the sidebar Settings.")
            return

        st.markdown('<div class="file-upload-section">', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "📁 Drag and drop transaction CSV files here",
            type=["csv"],
            accept_multiple_files=True,
            help="Upload one or more Saison transaction CSV files for processing",
            key="file_uploader"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Store uploaded files in session state to persist across reruns
        if uploaded_files:
            if "uploaded_files_cache" not in st.session_state:
                st.session_state.uploaded_files_cache = {}
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.uploaded_files_cache:
                    st.session_state.uploaded_files_cache[uploaded_file.name] = uploaded_file.getvalue()

        # Show count of files ready to process
        files_to_process = []
        if uploaded_files:
            files_to_process = uploaded_files
        elif "uploaded_files_cache" in st.session_state and st.session_state.uploaded_files_cache:
            # If uploader was cleared but we have cached files, show them
            st.info(f"📁 {len(st.session_state.uploaded_files_cache)} file(s) cached and ready to process")

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded and ready")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Process All Files", type="primary", width="stretch"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for idx, uploaded_file in enumerate(uploaded_files):
                        try:
                            status_text.text(f"Processing {uploaded_file.name}...")

                            df, encoding, pre_header = process_uploaded_file(
                                uploaded_file, min_attendees, max_attendees, id_2_weight, id_1_weight,
                                use_amount_based, amount_brackets, cost_per_person
                            )

                            # Store in preview data instead of processed
                            st.session_state.preview_data[uploaded_file.name] = {
                                "data": df,
                                "encoding": encoding,
                                "pre_header": pre_header,
                            }

                            st.success(f"✅ Processed {uploaded_file.name} - Ready for preview")

                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {e}")

                        progress_bar.progress((idx + 1) / len(uploaded_files))

                    status_text.text("✨ Processing complete! Click a file to preview and edit.")

            # Show preview files
            if st.session_state.preview_data:
                st.subheader("📋 Ready for Preview")

                # If a file is selected for preview, show the editor
                if st.session_state.current_preview_file and st.session_state.current_preview_file in st.session_state.preview_data:
                    render_preview_editor(st.session_state.current_preview_file)
                else:
                    # Show list of files to preview
                    for filename, data in st.session_state.preview_data.items():
                        df = data["data"]
                        encoding = data["encoding"]
                        relevant_count = (df["人数"] != "").sum()

                        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                        with col1:
                            st.text(filename)
                        with col2:
                            st.metric("Rows", len(df))
                        with col3:
                            st.metric("Relevant", relevant_count)
                        with col4:
                            st.metric("Encoding", encoding)
                        with col5:
                            if st.button("👁️ Preview", key=f"preview_{filename}"):
                                st.session_state.current_preview_file = filename
                                st.rerun()

            # Show processing summary
            if st.session_state.processed_data:
                st.subheader("✅ Confirmed Files")
                for filename, data in st.session_state.processed_data.items():
                    df = data["data"]
                    encoding = data["encoding"]
                    relevant_count = (df["人数"] != "").sum()
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("File", filename)
                    col2.metric("Rows", len(df))
                    col3.metric("Relevant", relevant_count)
                    col4.metric("Encoding", encoding)

    with tab2:
        st.header("Preview & Edit Data")

        if not st.session_state.preview_data:
            st.info("📝 No files processed yet. Upload files in the previous tab.")
        else:
            # Show file selector
            if not st.session_state.current_preview_file:
                st.subheader("Select a file to preview:")
                for filename in st.session_state.preview_data.keys():
                    if st.button(f"📄 {filename}", key=f"select_{filename}", width="stretch"):
                        st.session_state.current_preview_file = filename
                        st.rerun()
            else:
                # Show preview editor
                render_preview_editor(st.session_state.current_preview_file)

    with tab3:
        st.header("Download Results")

        if not st.session_state.processed_data:
            st.info("💾 No confirmed files available. Go back to Preview & Edit tab to confirm files.")
        else:
            # Download All & Reset button
            st.markdown("### 📦 Batch Download")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.info(f"📊 {len(st.session_state.processed_data)} file(s) ready to download")
            with col2:
                # Create zip file with all CSVs
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for filename, data_dict in st.session_state.processed_data.items():
                        df = data_dict["data"]
                        pre_header = data_dict["pre_header"]

                        # Create CSV content
                        csv_buffer = io.StringIO()
                        if pre_header:
                            for row in pre_header:
                                csv_buffer.write(",".join(str(val) for val in row) + "\n")
                        df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
                        csv_data = csv_buffer.getvalue()

                        # Add to zip
                        zip_file.writestr(filename, csv_data.encode('utf-8-sig'))

                zip_buffer.seek(0)

                st.download_button(
                    label="📦 Download All & Reset",
                    data=zip_buffer.getvalue(),
                    file_name="processed_files.zip",
                    mime="application/zip",
                    help="Download all processed files as a ZIP archive and reset the session",
                    type="primary",
                    width="stretch",
                    on_click=lambda: reset_session()
                )

            st.markdown("---")
            st.subheader("Individual Files")

            for filename, data_dict in st.session_state.processed_data.items():
                st.markdown(f"### {filename}")
                df = data_dict["data"]
                pre_header = data_dict["pre_header"]

                col1, col2 = st.columns(2)

                with col1:
                    csv_buffer = io.StringIO()
                    if pre_header:
                        for row in pre_header:
                            csv_buffer.write(",".join(str(val) for val in row) + "\n")
                    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
                    csv_data = csv_buffer.getvalue()

                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=filename,
                        mime="text/csv",
                        key=f"csv_{filename}",
                    )

                with col2:
                    if st.session_state.attendee_ref is not None:
                        try:
                            html_output = Path(f"/tmp/{filename.replace('.csv', '.html')}")

                            generate_html_report(
                                transactions=df,
                                attendee_reference=st.session_state.attendee_ref,
                                output_path=html_output,
                                source_filename=filename,
                                pre_header_rows=pre_header,
                                handle_duplicates=False,
                            )

                            with open(html_output, "r", encoding="utf-8") as f:
                                html_data = f.read()

                            st.download_button(
                                label="📥 Download HTML Report",
                                data=html_data,
                                file_name=filename.replace(".csv", ".html"),
                                mime="text/html",
                                key=f"html_{filename}",
                            )

                            html_output.unlink()

                        except Exception as e:
                            st.error(f"Error generating HTML: {e}")

                st.markdown("---")

    with tab4:
        render_attendee_management()


if __name__ == "__main__":
    main()
