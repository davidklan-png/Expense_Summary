"""Streamlit Web Interface for Saison Transform - Two-Step Workflow.

Interactive web application with vertical scroll-based workflow:
1. Upload - File upload with drag & drop
2. Process & Edit - Review, edit, and generate PDF report
"""

import sys
import tempfile
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from saisonxform.config import Config
from saisonxform.io import read_csv_with_detection
from saisonxform.reporting import get_unique_attendees
from saisonxform.selectors import estimate_attendee_count, sample_attendee_ids
from saisonxform.ui.step_process import render_process_edit_step
from saisonxform.ui.step_upload import render_upload_step
from saisonxform.ui.sticky_header import render_sticky_header
from saisonxform.ui.workflow_state import initialize_workflow_state
from saisonxform.ui.workflow_styles import get_auto_scroll_script, get_workflow_styles

# Page configuration
st.set_page_config(
    page_title="Saison Transform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom workflow styles
st.markdown(get_workflow_styles(), unsafe_allow_html=True)


def initialize_session_state() -> None:
    """Initialize session state variables."""
    initialize_workflow_state()

    if "attendee_ref" not in st.session_state:
        st.session_state["attendee_ref"] = None
    if "attendee_ref_path" not in st.session_state:
        st.session_state["attendee_ref_path"] = None
    if "config" not in st.session_state:
        config_path = Path("data/reference/config.toml")
        if config_path.exists():
            st.session_state["config"] = Config(config_file=config_path)
        else:
            st.session_state["config"] = Config()
    if "processed_files" not in st.session_state:
        st.session_state["processed_files"] = {}
    if "uploaded_files_cache" not in st.session_state:
        st.session_state["uploaded_files_cache"] = {}


def load_attendee_reference(reference_path: Path) -> Optional[pd.DataFrame]:
    """Load attendee reference CSV."""
    if not reference_path.exists():
        return None
    return pd.read_csv(reference_path, encoding="utf-8")


def process_file(filename: str, file_bytes: bytes) -> dict[str, Any]:
    """Process a single uploaded file.

    Args:
        filename: Name of the file
        file_bytes: File content as bytes

    Returns:
        Dictionary with keys: 'df', 'encoding', 'pre_header', 'unique_attendees'
    """
    # Get processing parameters from session state
    config = st.session_state["config"]
    min_attendees = config.min_attendees if config else 2
    max_attendees = config.max_attendees if config else 8

    # Amount-based settings
    use_amount_based = False
    amount_brackets = None
    cost_per_person = 3000

    if config and config.amount_based_attendees:
        use_amount_based = True
        amount_brackets = config.amount_based_attendees.get("brackets")
        cost_per_person = config.amount_based_attendees.get("cost_per_person", 3000)

    # Core member settings
    core_fill_strategy = "random"
    if config and config.core_fill_strategy:
        core_fill_strategy = config.core_fill_strategy

    # Write to temp file securely
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp_file:
        tmp_file.write(file_bytes)
        temp_path = Path(tmp_file.name)

    try:
        # Process the file
        df, encoding, pre_header_rows = read_csv_with_detection(temp_path)
    finally:
        # Guaranteed cleanup
        temp_path.unlink(missing_ok=True)

    if df.empty:
        raise ValueError("File is empty")

    # Get attendee reference
    attendee_ref = st.session_state["attendee_ref"]
    if attendee_ref is None:
        raise ValueError("Attendee reference not loaded")

    available_ids = attendee_ref["ID"].astype(str).tolist()

    # Extract core member IDs from NameList.csv (Core column = 1)
    core_ids: list[str] | None = None
    if "Core" in attendee_ref.columns:
        core_ids = attendee_ref[attendee_ref["Core"] == 1]["ID"].astype(str).tolist()
        if not core_ids:
            # No core members defined - log warning and use all IDs
            core_ids = None

    # Create mask for relevant transactions
    has_date = df["利用日"].notna() if "利用日" in df.columns else pd.Series([False] * len(df))
    has_subject = df["科目＆No."].notna() if "科目＆No." in df.columns else pd.Series([False] * len(df))

    if "科目＆No." in df.columns:
        has_category = df["科目＆No."].str.contains("会議費|接待費", na=False, regex=True)
    else:
        has_category = pd.Series([False] * len(df))

    relevant_mask = has_date & has_subject & has_category

    # Initialize columns
    df["人数"] = ""
    for i in range(1, 9):
        df[f"ID{i}"] = ""

    # Process relevant transactions
    if relevant_mask.sum() > 0:
        for idx in df[relevant_mask].index:
            amount = df.loc[idx, "利用金額"]

            brackets_to_use = amount_brackets if use_amount_based else None

            count = estimate_attendee_count(
                amount,
                min_attendees=min_attendees,
                max_attendees=max_attendees,
                amount_brackets=brackets_to_use,
                cost_per_person=cost_per_person,
            )
            df.loc[idx, "人数"] = str(count)

            ids_result = sample_attendee_ids(
                count=count,
                available_ids=available_ids,
                core_ids=core_ids,
                core_fill_strategy=core_fill_strategy,
                return_dict=True,
            )
            if not isinstance(ids_result, dict):
                raise TypeError(
                    f"Expected dict from sample_attendee_ids with return_dict=True, "
                    f"got {type(ids_result).__name__}",
                )
            for i in range(1, 9):
                col_name = f"ID{i}"
                df.loc[idx, col_name] = ids_result[col_name]

    # Remove unwanted columns
    columns_to_drop = ["本人・家族区分", "締前入金区分"]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    # Add blank 備考 column
    if "備考" not in df.columns:
        df["備考"] = ""

    # Get unique attendees
    unique_attendees = get_unique_attendees(df, st.session_state["attendee_ref"])

    return {
        "df": df,
        "encoding": encoding,
        "pre_header": pre_header_rows,
        "unique_attendees": unique_attendees,
    }


def render_editor(filename: str) -> None:
    """Render the editor interface for a file."""
    if filename not in st.session_state["processed_files"]:
        st.error("File data not found")
        return

    file_data = st.session_state["processed_files"][filename]
    df = file_data["df"].copy()

    # Convert all columns to strings for consistent editing, handling NaN values
    for col in df.columns:
        df[col] = df[col].fillna("").astype(str)

    unique_attendees = file_data.get("unique_attendees", [])

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        # Filter out empty strings and 'nan' string values
        relevant_count = ((df["人数"] != "") & (df["人数"] != "nan")).sum()
        st.metric("Processed Transactions", relevant_count)
    with col3:
        st.metric("Unique Attendees", len(unique_attendees))

    st.markdown("---")

    # Show preview with filtering
    show_all = st.checkbox("Show all rows", value=False, key=f"show_all_{filename}")

    if show_all:
        display_df = df
    else:
        # Show only rows with attendee data (filter out empty and 'nan' strings)
        display_df = df[(df["人数"] != "") & (df["人数"] != "nan")]

    # Use data_editor for editable DataFrame with disabled columns for auto-calculated fields
    column_config = {
        "人数": st.column_config.NumberColumn(
            "人数",
            help="Auto-calculated from ID columns",
            disabled=True,
        ),
    }

    edited_df = st.data_editor(
        display_df,
        width="stretch",
        height=400,
        num_rows="dynamic",  # Allow adding/deleting rows
        key=f"editor_{filename}",
        column_config=column_config,
    )

    # Calculate 人数 based on non-empty ID columns
    id_columns = [f"ID{i}" for i in range(1, 9)]
    for idx in edited_df.index:
        # Count non-empty ID values
        count = sum(
            1 for col in id_columns if col in edited_df.columns and edited_df.loc[idx, col] not in ["", "nan", None]
        )
        edited_df.loc[idx, "人数"] = str(count) if count > 0 else ""

    # Update the session state with edited data if changes were made
    if not edited_df.equals(display_df):
        # Merge changes back into full dataframe
        if show_all:
            st.session_state["processed_files"][filename]["df"] = edited_df.copy()
        else:
            # Update only the edited rows in the full dataframe
            df.update(edited_df)
            st.session_state["processed_files"][filename]["df"] = df.copy()

        # Recalculate unique attendees
        st.session_state["processed_files"][filename]["unique_attendees"] = get_unique_attendees(
            st.session_state["processed_files"][filename]["df"],
            st.session_state["attendee_ref"],
        )
        st.rerun()

    # Unique attendees list
    if unique_attendees is not None and len(unique_attendees) > 0:
        with st.expander(f"👥 Unique Attendees ({len(unique_attendees)})", expanded=False):
            if isinstance(unique_attendees, list):
                attendee_df = pd.DataFrame(unique_attendees)
            else:
                attendee_df = unique_attendees
            st.dataframe(attendee_df, width="stretch", hide_index=True)


def main() -> None:
    """Main application entry point."""
    initialize_session_state()

    # Auto-load attendee reference on first run
    if st.session_state["attendee_ref"] is None:
        try:
            ref_path = Path("data/reference/NameList.csv")
            if ref_path.exists():
                attendee_ref = load_attendee_reference(ref_path)
                if attendee_ref is not None:
                    st.session_state["attendee_ref"] = attendee_ref
                    st.session_state["attendee_ref_path"] = ref_path
        except (FileNotFoundError, PermissionError, ValueError):
            # Reference file not found or unreadable - user can upload manually
            pass

    # Render sticky header
    render_sticky_header()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Attendee list status
        if st.session_state["attendee_ref"] is not None:
            st.success(f"✅ {len(st.session_state['attendee_ref'])} attendees loaded")
            if st.session_state["attendee_ref_path"]:
                st.caption(f"📄 {st.session_state['attendee_ref_path'].name}")
        else:
            st.warning("⚠️ No attendee list loaded")

        # Attendee List settings
        with st.expander("📂 Attendee List", expanded=False):
            reference_dir = st.text_input(
                "Reference Directory",
                value=str(Path("data/reference")),
                help="Directory containing NameList.csv",
            )

            if st.button("🔄 Reload Attendee List"):
                try:
                    ref_path = Path(reference_dir) / "NameList.csv"
                    attendee_ref = load_attendee_reference(ref_path)
                    if attendee_ref is not None:
                        st.session_state["attendee_ref"] = attendee_ref
                        st.session_state["attendee_ref_path"] = ref_path
                        st.success(f"✅ Loaded {len(attendee_ref)} attendees")
                        st.rerun()
                    else:
                        st.error("❌ NameList.csv not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        # Display attendee list reference
        if st.session_state["attendee_ref"] is not None:
            st.markdown("---")
            st.subheader("👥 Attendee Reference")

            # Check if Core column exists and display accordingly
            if "Core" in st.session_state["attendee_ref"].columns:
                # Show core count
                core_count = (st.session_state["attendee_ref"]["Core"] == 1).sum()
                total_count = len(st.session_state["attendee_ref"])
                st.caption(f"⭐ Core: {core_count} | All: {total_count}")

                # Display ID, Name, and Core indicator
                attendee_display = st.session_state["attendee_ref"][["ID", "Name", "Core"]].copy()
                attendee_display["Core"] = attendee_display["Core"].apply(lambda x: "⭐" if x == 1 else "")
                attendee_display.columns = ["ID", "Name", ""]
            else:
                # No Core column - show ID and Name only
                attendee_display = st.session_state["attendee_ref"][["ID", "Name"]].copy()

            st.dataframe(attendee_display, width="stretch", hide_index=True, height=400)

    # Main content - vertical workflow
    # Step 1: Upload
    render_upload_step()

    # Step 2: Process & Edit (includes PDF generation)
    render_process_edit_step(process_file, render_editor)

    # Auto-scroll to current step
    if "scroll_to_step" in st.session_state and st.session_state["scroll_to_step"]:
        st.markdown(
            get_auto_scroll_script(st.session_state["scroll_to_step"]),
            unsafe_allow_html=True,
        )
        st.session_state["scroll_to_step"] = None


if __name__ == "__main__":
    main()
