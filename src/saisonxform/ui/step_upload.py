"""Step 1: Upload Component.

File upload interface with drag-and-drop support and validation.
"""

from typing import List, Optional

import streamlit as st

from .translations import get_text
from .workflow_state import WorkflowStep, advance_to_next_step, get_current_step


def render_upload_step():
    """Render the file upload step."""
    current_step = get_current_step()

    # Section header
    st.markdown(
        f"""
        <div class="workflow-section animate-in" id="step-1">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">1</span>
                    {get_text('upload.title')}
                </h2>
                <p class="section-description">
                    {get_text('upload.description')}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check if attendee list is loaded
    if st.session_state.attendee_ref is None:
        st.error(get_text('upload.error_no_attendee'))
        return

    # Upload zone with prominent file uploader
    st.markdown(f"### 📁 {get_text('upload.select_files')}")
    st.caption(get_text('upload.zone_caption'))

    uploaded_files = st.file_uploader(
        get_text('upload.csv_files'),
        type=["csv"],
        accept_multiple_files=True,
        help=get_text('upload.help'),
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
        st.markdown(f"### 📋 {get_text('upload.uploaded_files')}")

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
        st.success(get_text('upload.files_ready', count=len(uploaded_files)))

        # Automatically advance to next step (only if still on upload step)
        if current_step == WorkflowStep.UPLOAD:
            advance_to_next_step()
            st.rerun()

    # Show cached files if uploader was cleared
    elif "uploaded_files_cache" in st.session_state and st.session_state.uploaded_files_cache:
        st.info(get_text('upload.files_cached', count=len(st.session_state.uploaded_files_cache)))

        if st.button(get_text('upload.clear_cached'), type="secondary"):
            st.session_state.uploaded_files_cache = {}
            st.rerun()

    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
