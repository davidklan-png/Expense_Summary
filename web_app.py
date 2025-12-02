"""Streamlit Web Interface for Saison Transform - Three-Step Workflow.

Interactive web application with vertical scroll-based workflow:
1. Upload - File upload with drag & drop
2. Process & Edit - Review and edit processed data
3. Download - Download results in multiple formats
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
from saisonxform.io import read_csv_with_detection
from saisonxform.reporting import generate_html_report, get_unique_attendees
from saisonxform.selectors import estimate_attendee_count, sample_attendee_ids
from saisonxform.ui.sticky_header import render_sticky_header
from saisonxform.ui.step_download import render_download_step
from saisonxform.ui.step_process import render_process_edit_step
from saisonxform.ui.step_upload import render_upload_step
from saisonxform.ui.workflow_state import (
    WorkflowStep,
    get_current_step,
    initialize_workflow_state,
)
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


def initialize_session_state():
    """Initialize session state variables."""
    initialize_workflow_state()

    if "attendee_ref" not in st.session_state:
        st.session_state.attendee_ref = None
    if "attendee_ref_path" not in st.session_state:
        st.session_state.attendee_ref_path = None
    if "config" not in st.session_state:
        config_path = Path("data/reference/config.toml")
        if config_path.exists():
            st.session_state.config = Config(config_file=config_path)
        else:
            st.session_state.config = Config()
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = {}
    if "uploaded_files_cache" not in st.session_state:
        st.session_state.uploaded_files_cache = {}


def load_attendee_reference(reference_path: Path) -> Optional[pd.DataFrame]:
    """Load attendee reference CSV."""
    if not reference_path.exists():
        return None
    return pd.read_csv(reference_path, encoding="utf-8")


def process_file(filename: str, file_bytes: bytes) -> dict:
    """Process a single uploaded file.

    Args:
        filename: Name of the file
        file_bytes: File content as bytes

    Returns:
        Dictionary with processed data
    """
    # Get processing parameters from session state
    config = st.session_state.config
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

    # ID weights
    id_2_weight = 0.9
    id_1_weight = 0.1
    if config and config.primary_id_weights:
        id_2_weight = float(config.primary_id_weights.get("2", 0.9))
        id_1_weight = float(config.primary_id_weights.get("1", 0.1))

    # Write to temp file
    temp_path = Path(f"/tmp/{filename}")
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    # Process the file
    df, encoding, pre_header_rows = read_csv_with_detection(temp_path)
    temp_path.unlink()

    if df.empty:
        raise ValueError("File is empty")

    # Get attendee reference
    attendee_ref = st.session_state.attendee_ref
    if attendee_ref is None:
        raise ValueError("Attendee reference not loaded")

    available_ids = attendee_ref["ID"].astype(str).tolist()

    # Create mask for relevant transactions
    has_date = df["利用日"].notna() if "利用日" in df.columns else pd.Series([False] * len(df))
    has_subject = df["科目＆No."].notna() if "科目＆No." in df.columns else pd.Series([False] * len(df))
    relevant_mask = has_date & has_subject & df["科目＆No."].str.contains("会議費|接待費", na=False, regex=True)

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
            df.loc[idx, "人数"] = count

            ids_result = sample_attendee_ids(
                count=count,
                available_ids=available_ids,
                id_2_weight=id_2_weight,
                id_1_weight=id_1_weight,
                return_dict=True,
            )
            assert isinstance(ids_result, dict)
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
    unique_attendees = get_unique_attendees(df, st.session_state.attendee_ref)

    return {
        "df": df,
        "encoding": encoding,
        "pre_header": pre_header_rows,
        "unique_attendees": unique_attendees,
    }


def render_editor(filename: str):
    """Render the editor interface for a file."""
    if filename not in st.session_state.processed_files:
        st.error("File data not found")
        return

    file_data = st.session_state.processed_files[filename]
    df = file_data["df"].copy()
    encoding = file_data["encoding"]
    unique_attendees = file_data.get("unique_attendees", [])

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        relevant_count = (df["人数"] != "").sum()
        st.metric("Processed Transactions", relevant_count)
    with col3:
        st.metric("Unique Attendees", len(unique_attendees))

    st.markdown("---")

    # Show preview with filtering
    show_all = st.checkbox("Show all rows", value=False, key=f"show_all_{filename}")

    if show_all:
        display_df = df
    else:
        # Show only rows with attendee data
        display_df = df[df["人数"] != ""]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
    )

    # Unique attendees list
    if unique_attendees is not None and len(unique_attendees) > 0:
        with st.expander(f"👥 Unique Attendees ({len(unique_attendees)})", expanded=False):
            if isinstance(unique_attendees, list):
                attendee_df = pd.DataFrame(unique_attendees)
            else:
                attendee_df = unique_attendees
            st.dataframe(attendee_df, use_container_width=True, hide_index=True)


def generate_report(file_data: dict) -> str:
    """Generate HTML report for a file."""
    # Create temp output path
    temp_output = Path(f"/tmp/temp_report_{id(file_data)}.html")

    # Generate HTML report to temp file
    output_path = generate_html_report(
        transactions=file_data["df"],
        attendee_reference=st.session_state.attendee_ref,
        output_path=temp_output,
        source_filename="processed_data.csv",
        pre_header_rows=file_data.get("pre_header", []),
    )

    # Read the HTML content
    html_content = output_path.read_text(encoding="utf-8")

    # Clean up temp file
    output_path.unlink()

    return html_content


def main():
    """Main application entry point."""
    initialize_session_state()

    # Auto-load attendee reference on first run
    if st.session_state.attendee_ref is None:
        try:
            ref_path = Path("data/reference/NameList.csv")
            if ref_path.exists():
                attendee_ref = load_attendee_reference(ref_path)
                if attendee_ref is not None:
                    st.session_state.attendee_ref = attendee_ref
                    st.session_state.attendee_ref_path = ref_path
        except Exception:
            pass

    # Render sticky header
    render_sticky_header()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Attendee list status
        if st.session_state.attendee_ref is not None:
            st.success(f"✅ {len(st.session_state.attendee_ref)} attendees loaded")
            if st.session_state.attendee_ref_path:
                st.caption(f"📄 {st.session_state.attendee_ref_path.name}")
        else:
            st.warning("⚠️ No attendee list loaded")

        # Reference data settings
        with st.expander("📂 Reference Data", expanded=False):
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
                        st.session_state.attendee_ref = attendee_ref
                        st.session_state.attendee_ref_path = ref_path
                        st.success(f"✅ Loaded {len(attendee_ref)} attendees")
                        st.rerun()
                    else:
                        st.error("❌ NameList.csv not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # Main content - vertical workflow
    current_step = get_current_step()

    # Step 1: Upload
    render_upload_step()

    # Step 2: Process & Edit
    render_process_edit_step(process_file, render_editor)

    # Step 3: Download
    render_download_step(generate_report)

    # Auto-scroll to current step
    if "scroll_to_step" in st.session_state and st.session_state.scroll_to_step:
        st.markdown(
            get_auto_scroll_script(st.session_state.scroll_to_step),
            unsafe_allow_html=True,
        )
        st.session_state.scroll_to_step = None


if __name__ == "__main__":
    main()
