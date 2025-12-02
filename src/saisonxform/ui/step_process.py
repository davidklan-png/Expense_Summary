"""Step 2: Process & Edit Component.

File processing, preview, and editing interface.
"""

import pandas as pd
import streamlit as st

from .workflow_state import WorkflowStep, advance_to_next_step, can_access_step, is_step_complete, get_current_step


def render_process_edit_step(process_file_callback, render_editor_callback):
    """Render the process and edit step.

    Args:
        process_file_callback: Function to process uploaded files
        render_editor_callback: Function to render the editor interface
    """
    # Check if this step is accessible
    if not can_access_step(WorkflowStep.PROCESS_EDIT):
        st.markdown(
            """
            <div class="workflow-section section-locked" id="step-2">
                <div class="section-header">
                    <h2 class="section-title">
                        <span class="section-number">2</span>
                        Review & Edit
                    </h2>
                    <p class="section-description">
                        Process files and review the generated data. Edit attendee information and preview results.
                    </p>
                </div>
            </div>
            <div class="section-divider"></div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Section header
    st.markdown(
        """
        <div class="workflow-section animate-in" id="step-2">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">2</span>
                    Review & Edit
                </h2>
                <p class="section-description">
                    Process your files and review the generated data. Edit attendee information as needed.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check if files need processing
    processed_files = st.session_state.get("processed_files", {})
    uploaded_cache = st.session_state.get("uploaded_files_cache", {})

    if not uploaded_cache:
        st.warning("⚠️ No files uploaded. Please return to Step 1 to upload files.")
        return

    # Determine which files need processing
    unprocessed_files = [
        filename
        for filename in uploaded_cache.keys()
        if filename not in processed_files
    ]

    # Process files automatically if needed
    if unprocessed_files:
        st.markdown(
            f"""
            <div class="progress-container">
                <div class="progress-header">
                    <div class="progress-title">⏳ Processing Files</div>
                    <div class="progress-count">{len(unprocessed_files)} files</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, filename in enumerate(unprocessed_files):
            status_text.text(f"Processing {filename}...")
            progress_bar.progress((idx + 1) / len(unprocessed_files))

            try:
                # Call the processing callback
                result = process_file_callback(filename, uploaded_cache[filename])

                if result:
                    if "processed_files" not in st.session_state:
                        st.session_state.processed_files = {}
                    st.session_state.processed_files[filename] = result

            except Exception as e:
                st.error(f"❌ Error processing {filename}: {str(e)}")

        status_text.success("✅ All files processed!")
        progress_bar.empty()
        st.rerun()

    # Show editor if files are processed
    else:
        st.success(f"✅ **{len(processed_files)} file(s)** processed and ready for review")

        # File selector if multiple files
        if len(processed_files) > 1:
            selected_file = st.selectbox(
                "Select file to edit",
                options=list(processed_files.keys()),
                key="file_selector",
            )
        else:
            selected_file = list(processed_files.keys())[0]

        # Render the editor for the selected file
        if selected_file:
            with st.expander(f"📝 Edit: {selected_file}", expanded=True):
                render_editor_callback(selected_file)

        # Automatically advance to download (only if still on process/edit step)
        current_step = get_current_step()
        if current_step == WorkflowStep.PROCESS_EDIT:
            advance_to_next_step()
            st.rerun()

    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
