"""Step 3: Download Component.

Download processed files in various formats.
"""

import io
import zipfile
from pathlib import Path
from typing import Dict

import pandas as pd
import streamlit as st

from .workflow_state import WorkflowStep, can_access_step, reset_workflow


def render_download_step(generate_report_callback):
    """Render the download step.

    Args:
        generate_report_callback: Function to generate HTML reports
    """
    # Check if this step is accessible
    if not can_access_step(WorkflowStep.DOWNLOAD):
        st.markdown(
            """
            <div class="workflow-section section-locked" id="step-3">
                <div class="section-header">
                    <h2 class="section-title">
                        <span class="section-number">3</span>
                        Download Results
                    </h2>
                    <p class="section-description">
                        Download your processed files in various formats (CSV, Excel, HTML reports).
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Section header
    st.markdown(
        """
        <div class="workflow-section animate-in" id="step-3">
            <div class="section-header">
                <h2 class="section-title">
                    <span class="section-number">3</span>
                    Download Results
                </h2>
                <p class="section-description">
                    Your files are ready! Download them individually or as a batch.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    processed_files = st.session_state.get("processed_files", {})

    if not processed_files:
        st.warning("⚠️ No processed files available. Please return to Step 2.")
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📁 Files Processed", len(processed_files))

    with col2:
        total_rows = sum(len(data["df"]) for data in processed_files.values() if "df" in data)
        st.metric("📊 Total Transactions", total_rows)

    with col3:
        total_attendees = sum(
            len(data.get("unique_attendees", [])) for data in processed_files.values()
        )
        st.metric("👥 Unique Attendees", total_attendees)

    with col4:
        st.metric("✅ Status", "Complete")

    st.markdown("---")

    # Download format selector
    download_format = st.radio(
        "Select Download Format",
        ["📊 CSV (Processed Data)", "📈 Excel (Enhanced)", "📄 HTML Report", "📦 All Formats (ZIP)"],
        horizontal=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Individual file downloads
    if download_format in ["📊 CSV (Processed Data)", "📈 Excel (Enhanced)", "📄 HTML Report"]:
        st.markdown("### Individual Downloads")

        for filename, file_data in processed_files.items():
            col_file, col_download = st.columns([3, 1])

            with col_file:
                st.markdown(f"**{filename}**")
                if "df" in file_data:
                    st.caption(f"{len(file_data['df'])} rows • {len(file_data['df'].columns)} columns")

            with col_download:
                if download_format == "📊 CSV (Processed Data)":
                    csv_data = file_data["df"].to_csv(index=False)
                    st.download_button(
                        "⬇️ CSV",
                        csv_data,
                        file_name=f"processed_{filename}",
                        mime="text/csv",
                        key=f"download_csv_{filename}",
                    )

                elif download_format == "📈 Excel (Enhanced)":
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                        file_data["df"].to_excel(writer, index=False, sheet_name="Transactions")
                    excel_data = excel_buffer.getvalue()

                    st.download_button(
                        "⬇️ Excel",
                        excel_data,
                        file_name=f"processed_{Path(filename).stem}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_excel_{filename}",
                    )

                elif download_format == "📄 HTML Report":
                    html_report = generate_report_callback(file_data)

                    st.download_button(
                        "⬇️ HTML",
                        html_report,
                        file_name=f"report_{Path(filename).stem}.html",
                        mime="text/html",
                        key=f"download_html_{filename}",
                    )

    # Batch download (ZIP)
    else:
        st.markdown("### Batch Download")
        st.info("📦 Download all files in a single ZIP archive containing CSV, Excel, and HTML reports.")

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
                "📦 Download All (ZIP)",
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
        if st.button("🔄 Process New Files", type="primary", use_container_width=True, key="reset_from_download"):
            reset_workflow()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
