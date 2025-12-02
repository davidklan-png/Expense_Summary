"""Step 1: Upload Component.

File upload interface with drag-and-drop support and validation.
"""

from typing import List, Optional

import streamlit as st

from .workflow_state import WorkflowStep, advance_to_next_step, get_current_step


def render_upload_step():
    """Render the file upload step."""
    current_step = get_current_step()

    # Section header
    st.markdown(
        """
        <div class="workflow-section animate-in" id="step-1">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">1</span>
                    Upload Your Files
                </h2>
                <p class="section-description">
                    Upload one or more Saison transaction CSV files to begin processing.
                    Drag and drop files or click to browse.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check if attendee list is loaded
    if st.session_state.attendee_ref is None:
        st.error(
            """
            ⚠️ **Attendee list not loaded!**

            Please load the attendee reference file (NameList.csv) from the sidebar Settings before uploading files.
            """,
        )
        return

    # Upload zone with prominent file uploader
    st.markdown("### 📁 Select Files")
    st.caption("Drag and drop files here or click 'Browse files' button • Accepts CSV files • Max 200MB per file")

    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="Upload Saison transaction CSV files for processing",
        key="file_uploader",
        label_visibility="collapsed",
    )

    # Store uploaded files in session state
    if uploaded_files:
        if "uploaded_files_cache" not in st.session_state:
            st.session_state.uploaded_files_cache = {}

        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files_cache:
                st.session_state.uploaded_files_cache[uploaded_file.name] = uploaded_file.getvalue()

        # Display uploaded files
        st.markdown("---")
        st.markdown("### 📋 Uploaded Files")

        for uploaded_file in uploaded_files:
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            col_icon, col_name, col_size = st.columns([1, 6, 2])

            with col_icon:
                st.markdown("📄")
            with col_name:
                st.markdown(f"**{uploaded_file.name}**")
            with col_size:
                st.caption(f"{file_size:.1f} KB")

        # File count summary
        st.success(f"✅ **{len(uploaded_files)} file(s)** ready for processing")

        # Automatically advance to next step (only if still on upload step)
        if current_step == WorkflowStep.UPLOAD:
            advance_to_next_step()
            st.rerun()

    # Show cached files if uploader was cleared
    elif "uploaded_files_cache" in st.session_state and st.session_state.uploaded_files_cache:
        st.info(f"📁 {len(st.session_state.uploaded_files_cache)} file(s) cached from previous upload")

        if st.button("🔄 Clear cached files", type="secondary"):
            st.session_state.uploaded_files_cache = {}
            st.rerun()

    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
