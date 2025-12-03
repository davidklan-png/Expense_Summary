"""Step 3: Download Component.

Download processed files in various formats.
"""

import io
import zipfile
from pathlib import Path
from typing import Dict

import pandas as pd
import streamlit as st

from .translations import get_text
from .workflow_state import WorkflowStep, can_access_step, reset_workflow


def render_download_step(generate_report_callback):
    """Render the download step.

    Args:
        generate_report_callback: Function to generate HTML reports
    """
    lang = st.session_state.get("language", "en")

    # Check if this step is accessible
    if not can_access_step(WorkflowStep.DOWNLOAD):
        st.markdown(
            f"""
            <div class="workflow-section section-locked" id="step-3">
                <div class="section-header">
                    <h2 class="section-title">
                        <span class="section-number">3</span>
                        {get_text('download_title', lang)}
                    </h2>
                    <p class="section-description">
                        {get_text('download_description', lang)}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Section header
    st.markdown(
        f"""
        <div class="workflow-section animate-in" id="step-3">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">3</span>
                    {get_text('download_title', lang)}
                </h2>
                <p class="section-description">
                    {get_text('download_ready', lang)}
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    processed_files = st.session_state.get("processed_files", {})

    if not processed_files:
        st.warning(get_text('warning_no_processed_files', lang))
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(get_text('metric_files_processed', lang), len(processed_files))

    with col2:
        total_rows = sum(len(data["df"]) for data in processed_files.values() if "df" in data)
        st.metric(get_text('metric_total_transactions', lang), total_rows)

    with col3:
        total_attendees = sum(
            len(data.get("unique_attendees", [])) for data in processed_files.values()
        )
        st.metric(get_text('metric_unique_attendees', lang), total_attendees)

    with col4:
        st.metric(get_text('metric_status', lang), get_text('status_complete', lang))

    st.markdown("---")

    # Download format selector
    download_format = st.radio(
        get_text('select_download_format', lang),
        [
            get_text('format_csv', lang),
            get_text('format_excel', lang),
            get_text('format_html', lang),
            get_text('format_zip', lang),
        ],
        horizontal=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Individual file downloads
    # Check against translated format strings
    format_csv_text = get_text('format_csv', lang)
    format_excel_text = get_text('format_excel', lang)
    format_html_text = get_text('format_html', lang)

    if download_format in [format_csv_text, format_excel_text, format_html_text]:
        st.markdown(f"### {get_text('individual_downloads', lang)}")

        for filename, file_data in processed_files.items():
            col_file, col_download = st.columns([3, 1])

            with col_file:
                st.markdown(f"**{filename}**")
                if "df" in file_data:
                    st.caption(f"{len(file_data['df'])} rows • {len(file_data['df'].columns)} columns")

            with col_download:
                if download_format == format_csv_text:
                    csv_data = file_data["df"].to_csv(index=False)
                    st.download_button(
                        get_text('download_csv_button', lang),
                        csv_data,
                        file_name=f"processed_{filename}",
                        mime="text/csv",
                        key=f"download_csv_{filename}",
                    )

                elif download_format == format_excel_text:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                        file_data["df"].to_excel(writer, index=False, sheet_name="Transactions")
                    excel_data = excel_buffer.getvalue()

                    st.download_button(
                        get_text('download_excel_button', lang),
                        excel_data,
                        file_name=f"processed_{Path(filename).stem}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_excel_{filename}",
                    )

                elif download_format == format_html_text:
                    html_report = generate_report_callback(file_data)

                    st.download_button(
                        get_text('download_html_button', lang),
                        html_report,
                        file_name=f"report_{Path(filename).stem}.html",
                        mime="text/html",
                        key=f"download_html_{filename}",
                    )

    # Batch download (ZIP)
    else:
        st.markdown(f"### {get_text('batch_download', lang)}")
        st.info(get_text('batch_download_info', lang))

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_data in processed_files.items():
                base_name = Path(filename).stem

                # Add CSV
                csv_data = file_data["df"].to_csv(index=False)
                zip_file.writestr(f"csv/processed_{filename}", csv_data)

                # Add Excel
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    file_data["df"].to_excel(writer, index=False, sheet_name="Transactions")
                zip_file.writestr(f"excel/{base_name}.xlsx", excel_buffer.getvalue())

                # Add HTML
                html_report = generate_report_callback(file_data)
                zip_file.writestr(f"reports/{base_name}.html", html_report)

        zip_data = zip_buffer.getvalue()

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                get_text('download_all_zip_button', lang),
                zip_data,
                file_name="saison_transform_results.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True,
                on_click=reset_workflow,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Reset button
    st.markdown("---")
    st.markdown('<div class="cta-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text('process_new_files_button', lang), type="primary", use_container_width=True, key="reset_from_download"):
            reset_workflow()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
