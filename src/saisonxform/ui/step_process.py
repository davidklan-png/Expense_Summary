"""Step 2: Process & Edit Component.

File processing, preview, editing interface, and PDF generation.
"""

import streamlit as st

from ..reporting import generate_pdf_bytes
from .translations import get_text
from .workflow_state import WorkflowStep, can_access_step


def render_process_edit_step(process_file_callback, render_editor_callback):
    """Render the process and edit step with PDF generation.

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
                        st.session_state["processed_files"] = {}
                    st.session_state["processed_files"][filename] = result

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

        # PDF Generation section
        st.markdown("---")

        # PDF generation for single or multiple files
        if len(processed_files) == 1:
            # Single file - immediate download
            filename = list(processed_files.keys())[0]
            file_data = processed_files[filename]

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    get_text("process.create_pdf"),
                    type="primary",
                    width='stretch',
                    key="create_pdf_single",
                ):
                    try:
                        # Generate PDF
                        pdf_bytes = generate_pdf_bytes(
                            transactions=file_data["df"],
                            attendee_reference=st.session_state["attendee_ref"],
                            source_filename=filename,
                            pre_header_rows=file_data.get("pre_header", []),
                        )

                        # Prepare download filename
                        pdf_filename = filename.replace(".csv", ".pdf")

                        # Trigger download
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes.getvalue(),
                            file_name=pdf_filename,
                            mime="application/pdf",
                            key="download_pdf_button",
                            width='stretch',
                        )
                        st.success(get_text("process.pdf_ready"))

                    except Exception as e:
                        st.error(get_text("process.pdf_error", error=str(e)))
        else:
            # Multiple files - allow individual PDF downloads
            st.markdown("### 📄 Generate PDF Reports")
            st.caption("Click to generate and download PDF for each file")

            for filename in processed_files.keys():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**{filename}**")
                with col2:
                    if st.button(
                        get_text("process.create_pdf"),
                        key=f"pdf_{filename}",
                        width='stretch',
                    ):
                        try:
                            file_data = processed_files[filename]
                            pdf_bytes = generate_pdf_bytes(
                                transactions=file_data["df"],
                                attendee_reference=st.session_state["attendee_ref"],
                                source_filename=filename,
                                pre_header_rows=file_data.get("pre_header", []),
                            )

                            pdf_filename = filename.replace(".csv", ".pdf")

                            st.download_button(
                                label=f"⬇️ {pdf_filename}",
                                data=pdf_bytes.getvalue(),
                                file_name=pdf_filename,
                                mime="application/pdf",
                                key=f"download_pdf_{filename}",
                                width='stretch',
                            )
                            st.success(get_text("process.pdf_ready"))
                            st.rerun()

                        except Exception as e:
                            st.error(get_text("process.pdf_error", error=str(e)))

    # Section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
