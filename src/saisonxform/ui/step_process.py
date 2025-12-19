"""Step 2: Process & Edit Component.

File processing, preview, and editing interface.
"""

import streamlit as st

from .translations import get_text
from .workflow_state import WorkflowStep, advance_to_next_step, can_access_step


def render_process_edit_step(process_file_callback, render_editor_callback):
    """Render the process and edit step.

    Args:
        process_file_callback: Function to process uploaded files
        render_editor_callback: Function to render the editor interface
    """
    # Check if this step is accessible
    if not can_access_step(WorkflowStep.PROCESS_EDIT):
        st.markdown(
            f"""
            <div class="workflow-section section-locked" id="step-2">
                <div class="section-header">
                    <h2 class="section-title">
                        <span class="section-number">2</span>
                        {get_text('process.title')}
                    </h2>
                    <p class="section-description">
                        {get_text('process.description')}
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
        f"""
        <div class="workflow-section animate-in" id="step-2">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">2</span>
                    {get_text('process.title')}
                </h2>
                <p class="section-description">
                    {get_text('process.description')}
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
        st.warning(get_text("process.warning_no_files"))
        return

    # Determine which files need processing
    unprocessed_files = [filename for filename in uploaded_cache.keys() if filename not in processed_files]

    # Process files automatically if needed
    if unprocessed_files:
        st.markdown(
            f"""
            <div class="progress-container">
                <div class="progress-header">
                    <div class="progress-title">⏳ {get_text('process.processing_files')}</div>
                    <div class="progress-count">{len(unprocessed_files)} {get_text('process.files_label')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, filename in enumerate(unprocessed_files):
            status_text.text(get_text("process.processing_file", filename=filename))
            progress_bar.progress((idx + 1) / len(unprocessed_files))

            try:
                # Call the processing callback
                result = process_file_callback(filename, uploaded_cache[filename])

                if result:
                    if "processed_files" not in st.session_state:
                        st.session_state.processed_files = {}
                    st.session_state.processed_files[filename] = result

            except Exception as e:
                st.error(get_text("process.error_processing", filename=filename, error=str(e)))

        status_text.success(get_text("process.all_processed"))
        progress_bar.empty()
        st.rerun()

    # Show editor if files are processed
    else:
        st.success(get_text("process.files_ready", count=len(processed_files)))

        # File selector if multiple files
        if len(processed_files) > 1:
            selected_file = st.selectbox(
                get_text("process.select_file"),
                options=list(processed_files.keys()),
                key="file_selector",
            )
        else:
            selected_file = list(processed_files.keys())[0]

        # Render the editor for the selected file
        if selected_file:
            with st.expander(get_text("process.edit_file", filename=selected_file), expanded=True):
                render_editor_callback(selected_file)

        # Manual advance button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                get_text("process.continue_to_download"),
                type="primary",
                use_container_width=True,
                key="advance_to_download",
            ):
                advance_to_next_step()
                st.rerun()

    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
